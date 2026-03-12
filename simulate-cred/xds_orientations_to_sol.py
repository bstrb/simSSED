#!/usr/bin/env python3
"""
xds_orientations_to_sol.py

Create per-image orientation matrices from an XDS folder (XDS.INP + GXPARM.XDS/XPARM.XDS)
and write them to a CrystFEL-style .sol file.

What you get:
  - orientations_R.sol  : 3x3 *rotation* matrices U(frame) (crystal-Cartesian -> lab)
  - orientations_UB.sol : 3x3 *orientation* matrices A(frame)=U(frame)@B (maps hkl -> reciprocal vector in lab, 1/Å)

Notes:
    - In (G)XPARM.XDS, UNIT_CELL_*_AXIS are the real-space unit cell axes (in Å) in the lab frame
        at the reference setting corresponding to STARTING_ANGLE / STARTING_FRAME.
  - Per-image spindle angle:
        phi(frame) = STARTING_ANGLE + OSCILLATION_RANGE * (frame - STARTING_FRAME)
    (XDS assumes a right-handed rotation about ROTATION_AXIS when proceeding to the next image.)

This script is designed so you can feed the output into your simulation notebook by setting:
  ORIENTATION_SOURCE="from_sol"
  ORIENTATION_MATRICES_KIND="R" (recommended) or "UB" if you want the A=U@B matrix.

Usage:
  python xds_orientations_to_sol.py /path/to/xds_folder
  python xds_orientations_to_sol.py /path/to/xds_folder --phi-mode mid --format R
"""

from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np

try:
    import gemmi
except Exception:
    gemmi = None


def _parse_xds_inp(xds_inp: Path) -> dict:
    """Parse the minimum fields we need from XDS.INP (DATA_RANGE)."""
    txt = xds_inp.read_text(errors="replace").splitlines()
    out = {}
    for line in txt:
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        # remove inline comments after !
        if "!" in line:
            line = line.split("!")[0].strip()

        if line.upper().startswith("DATA_RANGE"):
            # DATA_RANGE= 1 757
            nums = [int(x) for x in line.split("=")[1].split()]
            if len(nums) >= 2:
                out["data_range"] = (nums[0], nums[1])
    if "data_range" not in out:
        raise ValueError(f"Could not find DATA_RANGE in {xds_inp}")
    return out


def _read_gxparm(gxparm: Path) -> dict:
    """
    Read GXPARM.XDS / XPARM.XDS.

    Expected numeric layout (from XDS docs / common format):
      line2: starting_frame starting_angle oscillation_range rot_axis_x rot_axis_y rot_axis_z
      line3: wavelength beam_dir_x beam_dir_y beam_dir_z_or_k (XDS writes k=1/lambda)
      line4: spacegroup a b c alpha beta gamma
      line5-7: unit_cell_a_axis (3 floats), unit_cell_b_axis, unit_cell_c_axis  (Å in lab)
    """
    lines = gxparm.read_text(errors="replace").splitlines()
    if len(lines) < 7:
        raise ValueError(f"{gxparm} does not look like a valid (G)XPARM.XDS")

    # line indices: 0=header, 1.. = data
    l2 = [float(x) for x in lines[1].split()]
    starting_frame = int(l2[0])
    starting_angle = float(l2[1])
    osc_range      = float(l2[2])
    rot_axis       = np.array(l2[3:6], dtype=float)

    l3 = [float(x) for x in lines[2].split()]
    wavelength = float(l3[0])

    l4 = lines[3].split()
    spacegroup = int(l4[0])
    a, b, c = map(float, l4[1:4])
    alpha, beta, gamma = map(float, l4[4:7])

    a_axis = np.array([float(x) for x in lines[4].split()], dtype=float)
    b_axis = np.array([float(x) for x in lines[5].split()], dtype=float)
    c_axis = np.array([float(x) for x in lines[6].split()], dtype=float)

    return dict(
        starting_frame=starting_frame,
        starting_angle=starting_angle,
        oscillation_range=osc_range,
        rotation_axis=rot_axis,
        wavelength=wavelength,
        spacegroup=spacegroup,
        cell=(a, b, c, alpha, beta, gamma),
        cell_axes_lab=(a_axis, b_axis, c_axis),
    )


def _cell_A_cart(cell: tuple[float, float, float, float, float, float]) -> np.ndarray:
    """
    Real-space basis matrix A (3x3) in the standard crystal Cartesian convention:
      a along x
      b in x-y plane
      c with components (cx, cy, cz)
    Columns are a_cart, b_cart, c_cart (Å).
    """
    a, b, c, alpha, beta, gamma = cell
    ar = np.deg2rad(alpha)
    br = np.deg2rad(beta)
    gr = np.deg2rad(gamma)

    va = np.array([a, 0.0, 0.0], dtype=float)
    vb = np.array([b * np.cos(gr), b * np.sin(gr), 0.0], dtype=float)

    cx = c * np.cos(br)
    cy = c * (np.cos(ar) - np.cos(br) * np.cos(gr)) / np.sin(gr)
    cz_sq = c*c - cx*cx - cy*cy
    cz = np.sqrt(max(cz_sq, 0.0))
    vc = np.array([cx, cy, cz], dtype=float)

    A = np.stack([va, vb, vc], axis=1)  # columns
    return A


def _cell_B_recip(cell: tuple[float, float, float, float, float, float]) -> np.ndarray:
    """
    Reciprocal basis matrix B (3x3) without 2π, in the same crystal Cartesian convention as _cell_A_cart.
    Columns are a*, b*, c* in 1/Å.

    B = (A^{-1})^T
    """
    A = _cell_A_cart(cell)
    return np.linalg.inv(A).T


def _closest_rotation(M: np.ndarray) -> np.ndarray:
    """Project a 3x3 matrix to the nearest proper rotation matrix using SVD."""
    U, S, Vt = np.linalg.svd(M)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    return R


def _rodrigues(axis: np.ndarray, angle_rad: float) -> np.ndarray:
    """Rotation matrix for a right-handed rotation about 'axis' by angle_rad."""
    axis = np.array(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    x, y, z = axis
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    C = 1.0 - c
    return np.array([
        [c + x*x*C,   x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, c + y*y*C,   y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, c + z*z*C],
    ], dtype=float)


def _bravais_from_spacegroup(spacegroup: int) -> str:
    """
    Best-effort CrystFEL-style bravais string like cP, tI, oC, mP(b), hR, ...
    Uses gemmi if available; otherwise returns 'aP'.
    """
    if gemmi is None:
        return "aP"
    sg = gemmi.SpaceGroup(spacegroup)

    system = sg.crystal_system_str()  # triclinic, monoclinic, orthorhombic, tetragonal, trigonal, hexagonal, cubic
    cent = sg.centring_type()         # P, A, B, C, I, F, R

    lat_code = {
        "triclinic": "a",
        "monoclinic": "m",
        "orthorhombic": "o",
        "tetragonal": "t",
        "trigonal": "h",     # CrystFEL typically uses h for trigonal/hexagonal settings
        "hexagonal": "h",
        "cubic": "c",
    }.get(system, "a")

    # unique axis annotation (matches the convention used in your notebook)
    axis_map = {
        "monoclinic": "b",
        "tetragonal": "c",
        "trigonal": "c",
        "hexagonal": "c",
    }
    unique = axis_map.get(system, "")

    # If gemmi returns 'R' centering (rhombohedral), keep it: hR
    if unique:
        return f"{lat_code}{cent}{unique}"
    return f"{lat_code}{cent}"


def write_sol(
    out_path: Path,
    matrices: np.ndarray,
    bravais: str,
    ref_tag: str,
    note: str,
):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as fh:
        fh.write(f"# Generated by xds_orientations_to_sol.py\n")
        fh.write(f"# {note}\n")
        fh.write(f"# ref_tag={ref_tag}\n")
        fh.write(f"# format: <ref_tag> //<frame_index> m11 ... m33 0.000 0.000 <bravais>\n")
        for i, M in enumerate(matrices, start=1):
            vals = " ".join(f"{v:+.7f}" for v in M.reshape(-1))
            fh.write(f"{ref_tag} //{i} {vals} 0.000 0.000 {bravais}\n")


def read_sol_matrices(sol_path: Path) -> np.ndarray:
    """
    Read matrices from a CrystFEL-style .sol file.

    Expected row format:
      <tag> //<idx> m11 ... m33 0.000 0.000 <bravais>
    """
    mats = []
    with Path(sol_path).expanduser().open("r") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            floats = []
            for part in line.split():
                try:
                    floats.append(float(part))
                except ValueError:
                    continue
            if len(floats) >= 9:
                mats.append(np.array(floats[:9], dtype=float).reshape(3, 3))

    if not mats:
        raise ValueError(f"No orientation matrices found in: {sol_path}")

    return np.stack(mats, axis=0)


def generate_from_xds(
    xds_folder: str | Path,
    phi_mode: str = "mid",
    fmt: str = "both",
    ref_tag: str = "XDS",
    out_prefix: str = "orientations",
    frame_offset: int = 0,
    angle_offset_deg: float = 0.0,
    rotation_sign: int = 1,
) -> dict:
    """
    Generate orientation .sol files from an XDS folder.

    Returns:
      {
        "folder": Path,
        "bravais": str,
        "n_orientations": int,
        "format": str,
        "paths": {"R": Path | None, "UB": Path | None}
      }
    """
    folder = Path(xds_folder).expanduser().resolve()
    xds_inp = folder / "XDS.INP"
    if not xds_inp.exists():
        raise FileNotFoundError(f"Missing {xds_inp}")

    gxparm = folder / "GXPARM.XDS"
    if not gxparm.exists():
        gxparm = folder / "XPARM.XDS"
    if not gxparm.exists():
        raise FileNotFoundError(f"Missing GXPARM.XDS or XPARM.XDS in {folder}")

    if phi_mode not in ("start", "mid"):
        raise ValueError("phi_mode must be 'start' or 'mid'")

    if int(rotation_sign) not in (-1, 1):
        raise ValueError("rotation_sign must be +1 or -1")

    fmt = fmt.upper()
    if fmt not in ("R", "UB", "BOTH"):
        raise ValueError("fmt must be 'R', 'UB', or 'both'")

    inp = _parse_xds_inp(xds_inp)
    gx = _read_gxparm(gxparm)

    first, last = inp["data_range"]
    n = last - first + 1
    if n <= 0:
        raise ValueError(f"Bad DATA_RANGE in {xds_inp}: {first} {last}")

    start_frame = gx["starting_frame"]
    start_angle = gx["starting_angle"]
    osc = gx["oscillation_range"]
    axis = gx["rotation_axis"]
    axis = axis / np.linalg.norm(axis)

    cell = gx["cell"]
    a_axis_lab, b_axis_lab, c_axis_lab = gx["cell_axes_lab"]
    A0_lab = np.stack([a_axis_lab, b_axis_lab, c_axis_lab], axis=1)

    A_cart = _cell_A_cart(cell)
    U0 = A0_lab @ np.linalg.inv(A_cart)
    U0 = _closest_rotation(U0)

    B = _cell_B_recip(cell)

    source_frames = np.arange(first, last + 1, dtype=int)
    frames = source_frames.astype(float) + float(frame_offset)
    phi_abs = start_angle + osc * (frames - float(start_frame))
    if phi_mode == "mid":
        phi_abs = phi_abs + 0.5 * osc
    phi_abs = phi_abs + float(angle_offset_deg)

    # GXPARM axes correspond to the reference orientation at STARTING_ANGLE.
    # Apply only the relative spindle motion from that reference.
    phi_rel = (phi_abs - float(start_angle)) * float(int(rotation_sign))

    U_all = np.empty((n, 3, 3), dtype=float)
    for i, ang_deg in enumerate(phi_rel):
        Rax = _rodrigues(axis, np.deg2rad(ang_deg))
        U_all[i] = Rax @ U0

    bravais = _bravais_from_spacegroup(int(gx["spacegroup"]))

    note_common = (
        f"source={gxparm.name}, DATA_RANGE={first}-{last}, "
        f"STARTING_FRAME={start_frame}, STARTING_ANGLE={start_angle}, OSC_RANGE={osc}, "
        f"phi_mode={phi_mode}, frame_offset={int(frame_offset)}, angle_offset_deg={float(angle_offset_deg)}, "
        f"rotation_sign={int(rotation_sign)}"
    )

    out_r = None
    out_ub = None

    if fmt in ("R", "BOTH"):
        out_r = folder / f"{out_prefix}_R.sol"
        write_sol(
            out_r,
            U_all,
            bravais=bravais,
            ref_tag=ref_tag,
            note="Rotation matrices U(frame) (crystal Cartesian -> lab). " + note_common,
        )

    if fmt in ("UB", "BOTH"):
        A_all = U_all @ B
        out_ub = folder / f"{out_prefix}_UB.sol"
        write_sol(
            out_ub,
            A_all,
            bravais=bravais,
            ref_tag=ref_tag,
            note="Orientation matrices A(frame)=U(frame)@B (maps hkl -> reciprocal lab vector, 1/Å). " + note_common,
        )

    return {
        "folder": folder,
        "bravais": bravais,
        "n_orientations": int(n),
        "format": fmt,
        "data_range": (int(first), int(last)),
        "source_frame_numbers": source_frames.copy(),
        "mapped_frame_numbers": frames.astype(int),
        "starting_frame": int(start_frame),
        "starting_angle_deg": float(start_angle),
        "oscillation_range_deg": float(osc),
        "rotation_axis_unit": axis.copy(),
        "rotation_sign": int(rotation_sign),
        "frame_offset": int(frame_offset),
        "angle_offset_deg": float(angle_offset_deg),
        "first_phi_abs_deg": float(phi_abs[0]),
        "first_phi_rel_deg": float(phi_rel[0]),
        "phi_abs_degrees": phi_abs.copy(),
        "phi_rel_degrees": phi_rel.copy(),
        "paths": {
            "R": out_r,
            "UB": out_ub,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xds_folder", type=str, help="Folder containing XDS.INP and GXPARM.XDS (or XPARM.XDS).")
    ap.add_argument("--phi-mode", choices=["start", "mid"], default="mid",
                    help="Use start-of-image angle ('start') or midpoint angle ('mid'). Default: mid.")
    ap.add_argument("--format", choices=["R", "UB", "both"], default="both",
                    help="Write rotation matrices (R), orientation matrices (UB=U@B), or both. Default: both.")
    ap.add_argument("--ref-tag", default="XDS",
                    help="First token written in each .sol row (can be any string; parser usually ignores it).")
    ap.add_argument("--out-prefix", default="orientations",
                    help="Output prefix inside xds_folder (default: orientations -> orientations_R.sol etc).")
    ap.add_argument("--frame-offset", type=int, default=0,
                    help="Integer offset applied to DATA_RANGE frame numbers before computing phi.")
    ap.add_argument("--angle-offset-deg", type=float, default=0.0,
                    help="Additional angle offset [deg] added to all computed phi values.")
    ap.add_argument("--rotation-sign", type=int, default=1, choices=[-1, 1],
                    help="Sign for relative spindle rotation applied from STARTING_ANGLE (+1 or -1).")
    args = ap.parse_args()

    result = generate_from_xds(
        xds_folder=args.xds_folder,
        phi_mode=args.phi_mode,
        fmt=args.format,
        ref_tag=args.ref_tag,
        out_prefix=args.out_prefix,
        frame_offset=args.frame_offset,
        angle_offset_deg=args.angle_offset_deg,
        rotation_sign=args.rotation_sign,
    )
    print(
        f"Wrote {result['n_orientations']} orientations in {result['folder']} "
        f"(bravais={result['bravais']})."
    )


if __name__ == "__main__":
    main()
