\
"""
Minimal XDS geometry/orientation parser.

Goal: parse ONLY what is needed for diffraction simulation:
- GXPARM.XDS (classic XPARM block)
- optionally XDS.INP and/or XDS_ASCII.HKL header for image template / data range / reflecting-range parameters

This module intentionally ignores reflection tables (INTEGRATE.HKL etc).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

import re

import numpy as np

@dataclass(frozen=True)
class XDSGeometry:
    # Rotation / scan
    starting_frame: int
    starting_angle_deg: float
    oscillation_range_deg: float
    rotation_axis: np.ndarray  # (3,)

    # Beam
    wavelength_A: float
    incident_beam_dir: np.ndarray  # (3,) (will be normalized when used)

    # Crystal
    space_group_number: int
    unit_cell_constants: Tuple[float, float, float, float, float, float]  # a,b,c,alpha,beta,gamma
    a_axis_A: np.ndarray  # (3,)
    b_axis_A: np.ndarray  # (3,)
    c_axis_A: np.ndarray  # (3,)

    # Detector
    nx: int
    ny: int
    qx_mm: float
    qy_mm: float
    orgx_px: float
    orgy_px: float
    detector_distance_mm: float

    det_x: np.ndarray  # (3,) direction cosines in lab frame
    det_y: np.ndarray  # (3,)
    det_z: np.ndarray  # (3,) (usually det_x x det_y)

    # Optional: image template + range (from XDS.INP or XDS_ASCII.HKL header)
    name_template_of_data_frames: Optional[str] = None
    data_range: Optional[Tuple[int, int]] = None

    # Optional “profile” parameters (from XDS_ASCII.HKL header)
    include_resolution_range: Optional[Tuple[float, float]] = None  # (dmax, dmin) Å
    reflecting_range_esd_deg: Optional[float] = None
    beam_divergence_esd_deg: Optional[float] = None

    def beam_dir_unit(self) -> np.ndarray:
        v = np.array(self.incident_beam_dir, dtype=float)
        n = np.linalg.norm(v)
        if n == 0:
            raise ValueError("Incident beam direction vector has zero length.")
        return v / n

    def rotation_axis_unit(self) -> np.ndarray:
        v = np.array(self.rotation_axis, dtype=float)
        n = np.linalg.norm(v)
        if n == 0:
            raise ValueError("Rotation axis vector has zero length.")
        return v / n

    def direct_basis_A(self) -> np.ndarray:
        """3x3 matrix with direct axes as columns, in Å, in lab frame at the reference spindle angle."""
        return np.stack([self.a_axis_A, self.b_axis_A, self.c_axis_A], axis=1)

    def reciprocal_basis_invA(self) -> np.ndarray:
        """3x3 reciprocal basis (a*,b*,c* as columns) in 1/Å with the convention a·a* = 1 (no 2π)."""
        A = self.direct_basis_A()
        a, b, c = A[:, 0], A[:, 1], A[:, 2]
        v = float(np.dot(a, np.cross(b, c)))
        if abs(v) < 1e-12:
            raise ValueError("Unit cell volume is ~0; cannot form reciprocal basis.")
        astar = np.cross(b, c) / v
        bstar = np.cross(c, a) / v
        cstar = np.cross(a, b) / v
        return np.stack([astar, bstar, cstar], axis=1)

def _parse_numbers(line: str) -> list[float]:
    return [float(x) for x in line.split()]

def _parse_ints(line: str) -> list[int]:
    return [int(float(x)) for x in line.split()]

def parse_gxparm_xds(path: Path) -> XDSGeometry:
    """
    Parse classic fixed-format XPARM (GXPARM.XDS).

    Tested with the file layout:

    1: comment/header
    2: STARTING_FRAME STARTING_ANGLE OSC_RANGE ROT_AXIS(3)
    3: WAVELENGTH BEAM_DIR(3)      (beam dir might not be unit; we'll normalize later)
    4: SPACE_GROUP a b c alpha beta gamma
    5-7: UNIT_CELL_{A,B,C}-AXIS (3 each)
    8: SEGMENT_NUMBER NX NY QX QY
    9: ORGX ORGY DETECTOR_DISTANCE
    10-12: DETECTOR_XAXIS(3), DETECTOR_YAXIS(3), DETECTOR_ZAXIS(3)
    Remaining lines are ignored.
    """
    lines = path.read_text().splitlines()
    if len(lines) < 12:
        raise ValueError(f"GXPARM looks too short: {path}")

    # Line 2
    l2 = _parse_numbers(lines[1])
    if len(l2) != 6:
        raise ValueError(f"Unexpected number of values on line2: {len(l2)}")
    starting_frame = int(round(l2[0]))
    starting_angle_deg = float(l2[1])
    oscillation_range_deg = float(l2[2])
    rotation_axis = np.array(l2[3:6], dtype=float)

    # Line 3
    l3 = _parse_numbers(lines[2])
    if len(l3) != 4:
        raise ValueError(f"Unexpected number of values on line3: {len(l3)}")
    wavelength_A = float(l3[0])
    incident_beam_dir = np.array(l3[1:4], dtype=float)

    # Line 4
    l4 = _parse_numbers(lines[3])
    if len(l4) != 7:
        raise ValueError(f"Unexpected number of values on line4: {len(l4)}")
    space_group_number = int(round(l4[0]))
    unit_cell_constants = (float(l4[1]), float(l4[2]), float(l4[3]),
                           float(l4[4]), float(l4[5]), float(l4[6]))

    # Lines 5-7: direct axes
    a_axis_A = np.array(_parse_numbers(lines[4]), dtype=float)
    b_axis_A = np.array(_parse_numbers(lines[5]), dtype=float)
    c_axis_A = np.array(_parse_numbers(lines[6]), dtype=float)
    if a_axis_A.shape != (3,) or b_axis_A.shape != (3,) or c_axis_A.shape != (3,):
        raise ValueError("Unexpected UNIT_CELL_*_AXIS formatting in GXPARM.XDS")

    # Line 8: detector segment + size
    l8 = _parse_numbers(lines[7])
    if len(l8) != 5:
        raise ValueError(f"Unexpected number of values on line8: {len(l8)}")
    nx = int(round(l8[1]))
    ny = int(round(l8[2]))
    qx_mm = float(l8[3])
    qy_mm = float(l8[4])

    # Line 9: origin + distance
    l9 = _parse_numbers(lines[8])
    if len(l9) != 3:
        raise ValueError(f"Unexpected number of values on line9: {len(l9)}")
    orgx_px = float(l9[0])
    orgy_px = float(l9[1])
    detector_distance_mm = float(l9[2])

    # Lines 10-12: detector axes
    det_x = np.array(_parse_numbers(lines[9]), dtype=float)
    det_y = np.array(_parse_numbers(lines[10]), dtype=float)
    det_z = np.array(_parse_numbers(lines[11]), dtype=float)

    # Normalize detector axes (defensive)
    def _norm(v: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(v)
        if n == 0:
            raise ValueError("Zero-length detector axis vector in GXPARM.XDS")
        return v / n

    det_x = _norm(det_x)
    det_y = _norm(det_y)
    det_z = _norm(det_z)

    return XDSGeometry(
        starting_frame=starting_frame,
        starting_angle_deg=starting_angle_deg,
        oscillation_range_deg=oscillation_range_deg,
        rotation_axis=rotation_axis,
        wavelength_A=wavelength_A,
        incident_beam_dir=incident_beam_dir,
        space_group_number=space_group_number,
        unit_cell_constants=unit_cell_constants,
        a_axis_A=a_axis_A,
        b_axis_A=b_axis_A,
        c_axis_A=c_axis_A,
        nx=nx,
        ny=ny,
        qx_mm=qx_mm,
        qy_mm=qy_mm,
        orgx_px=orgx_px,
        orgy_px=orgy_px,
        detector_distance_mm=detector_distance_mm,
        det_x=det_x,
        det_y=det_y,
        det_z=det_z,
    )

def parse_xds_inp_minimal(path: Path) -> Dict[str, Any]:
    """
    Parse only a few keys from XDS.INP:
    - NAME_TEMPLATE_OF_DATA_FRAMES
    - DATA_RANGE
    - INCLUDE_RESOLUTION_RANGE (optional)
    """
    out: Dict[str, Any] = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("!"):
            continue
        # Remove inline comment after '!' if present
        if "!" in line:
            line = line.split("!", 1)[0].strip()
        if line.startswith("NAME_TEMPLATE_OF_DATA_FRAMES="):
            out["name_template_of_data_frames"] = line.split("=", 1)[1].strip()
        elif line.startswith("DATA_RANGE="):
            parts = line.split("=", 1)[1].split()
            if len(parts) >= 2:
                out["data_range"] = (int(parts[0]), int(parts[1]))
        elif line.startswith("INCLUDE_RESOLUTION_RANGE="):
            parts = line.split("=", 1)[1].split()
            if len(parts) >= 2:
                out["include_resolution_range"] = (float(parts[0]), float(parts[1]))
    return out

def parse_xds_ascii_header_minimal(path: Path) -> Dict[str, Any]:
    """
    Parse ONLY the header (lines starting with '!') from XDS_ASCII.HKL until !END_OF_HEADER.

    Useful because it records:
    - INCLUDE_RESOLUTION_RANGE
    - REFLECTING_RANGE_E.S.D.
    - BEAM_DIVERGENCE_E.S.D.
    - INCIDENT_BEAM_DIRECTION (unit)
    - ORGX/ORGY, DETECTOR_DISTANCE, QX/QY, etc.

    We do not read reflections.
    """
    out: Dict[str, Any] = {}
    def _find_labeled_number(text: str, label: str) -> Optional[float]:
        match = re.search(rf"\b{re.escape(label)}\s*=\s*([+-]?[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?)", text)
        if match:
            return float(match.group(1))
        return None

    with path.open("rt", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            if not raw.startswith("!"):
                # In practice header is entirely '!' lines; be safe.
                continue
            line = raw.strip()
            if line == "!END_OF_HEADER":
                break
            if "=" not in line:
                continue
            key, val = line[1:].split("=", 1)  # drop leading '!'
            key = key.strip()
            val = val.strip()
            # Handle a few keys we care about
            if key == "NAME_TEMPLATE_OF_DATA_FRAMES":
                out["name_template_of_data_frames"] = val
            elif key == "DATA_RANGE":
                parts = val.split()
                if len(parts) >= 2:
                    out["data_range"] = (int(parts[0]), int(parts[1]))
            elif key == "INCLUDE_RESOLUTION_RANGE":
                parts = val.split()
                if len(parts) >= 2:
                    out["include_resolution_range"] = (float(parts[0]), float(parts[1]))
            elif key == "REFLECTING_RANGE_E.S.D.":
                out["reflecting_range_esd_deg"] = float(val.split()[0])
            elif key == "BEAM_DIVERGENCE_E.S.D.":
                out["beam_divergence_esd_deg"] = float(val.split()[0])
            elif key == "INCIDENT_BEAM_DIRECTION":
                parts = val.split()
                if len(parts) >= 3:
                    out["incident_beam_dir_unit"] = np.array([float(parts[0]), float(parts[1]), float(parts[2])], dtype=float)
            elif key == "ROTATION_AXIS":
                parts = val.split()
                if len(parts) >= 3:
                    out["rotation_axis"] = np.array([float(parts[0]), float(parts[1]), float(parts[2])], dtype=float)
            elif key == "OSCILLATION_RANGE":
                out["oscillation_range_deg"] = float(val.split()[0])
            elif key == "STARTING_ANGLE":
                out["starting_angle_deg"] = float(val.split()[0])
            elif key == "STARTING_FRAME":
                out["starting_frame"] = int(float(val.split()[0]))
            elif key == "NX":
                # XDS_ASCII often encodes multiple labels on one line: NX= ... NY= ... QX= ... QY= ...
                nx = _find_labeled_number(raw, "NX")
                ny = _find_labeled_number(raw, "NY")
                qx = _find_labeled_number(raw, "QX")
                qy = _find_labeled_number(raw, "QY")
                if nx is not None:
                    out["nx"] = int(nx)
                if ny is not None:
                    out["ny"] = int(ny)
                if qx is not None:
                    out["qx_mm"] = float(qx)
                if qy is not None:
                    out["qy_mm"] = float(qy)
            elif key == "QX":
                parts = val.split()
                if len(parts) >= 2:
                    out["qx_mm"] = float(parts[0])
                    out["qy_mm"] = float(parts[1])
            elif key == "ORGX":
                # XDS_ASCII often encodes ORGX= ... ORGY= ... on one line
                orgx = _find_labeled_number(raw, "ORGX")
                orgy = _find_labeled_number(raw, "ORGY")
                if orgx is not None:
                    out["orgx_px"] = float(orgx)
                if orgy is not None:
                    out["orgy_px"] = float(orgy)
            elif key == "DETECTOR_DISTANCE":
                out["detector_distance_mm"] = float(val.split()[0])
            elif key == "DIRECTION_OF_DETECTOR_X-AXIS":
                parts = val.split()
                if len(parts) >= 3:
                    out["det_x"] = np.array([float(parts[0]), float(parts[1]), float(parts[2])], dtype=float)
            elif key == "DIRECTION_OF_DETECTOR_Y-AXIS":
                parts = val.split()
                if len(parts) >= 3:
                    out["det_y"] = np.array([float(parts[0]), float(parts[1]), float(parts[2])], dtype=float)
            elif key == "UNIT_CELL_A-AXIS":
                parts = val.split()
                if len(parts) >= 3:
                    out["a_axis_A"] = np.array([float(parts[0]), float(parts[1]), float(parts[2])], dtype=float)
            elif key == "UNIT_CELL_B-AXIS":
                parts = val.split()
                if len(parts) >= 3:
                    out["b_axis_A"] = np.array([float(parts[0]), float(parts[1]), float(parts[2])], dtype=float)
            elif key == "UNIT_CELL_C-AXIS":
                parts = val.split()
                if len(parts) >= 3:
                    out["c_axis_A"] = np.array([float(parts[0]), float(parts[1]), float(parts[2])], dtype=float)
            # Additional keys could be added if needed, but keep minimal by design.
    return out

def load_xds_geometry(xds_dir: str | Path, *,
                      gxparm_name: str = "GXPARM.XDS",
                      xds_inp_name: str = "XDS.INP",
                      xds_ascii_name: str = "XDS_ASCII.HKL",
                      prefer_ascii_header: bool = True) -> XDSGeometry:
    """
    Load XDS geometry from an XDS folder.

    Strategy:
    1) Parse GXPARM.XDS (required)
    2) Optionally patch in NAME_TEMPLATE/DATA_RANGE from XDS.INP or XDS_ASCII.HKL header
    3) Optionally patch in reflecting-range / beam-divergence from XDS_ASCII.HKL header
    """
    xds_dir = Path(xds_dir)
    gxparm_path = xds_dir / gxparm_name
    if not gxparm_path.exists():
        raise FileNotFoundError(f"Missing {gxparm_name} in {xds_dir}")

    geom = parse_gxparm_xds(gxparm_path)

    # Patch from XDS.INP (minimal keys)
    inp_path = xds_dir / xds_inp_name
    inp_data: Dict[str, Any] = {}
    if inp_path.exists():
        inp_data = parse_xds_inp_minimal(inp_path)

    # Patch from XDS_ASCII.HKL header (minimal keys)
    ascii_path = xds_dir / xds_ascii_name
    ascii_data: Dict[str, Any] = {}
    if ascii_path.exists():
        ascii_data = parse_xds_ascii_header_minimal(ascii_path)

    # Choose template/range: prefer ASCII header if requested
    def choose(key: str):
        if prefer_ascii_header and key in ascii_data:
            return ascii_data[key]
        if key in inp_data:
            return inp_data[key]
        if key in ascii_data:
            return ascii_data[key]
        return None

    name_template = choose("name_template_of_data_frames")
    data_range = choose("data_range")
    include_res = choose("include_resolution_range")

    # Optional geometry overrides from ASCII header
    rotation_axis = choose("rotation_axis")
    if rotation_axis is None:
        rotation_axis = geom.rotation_axis
    starting_angle_deg = choose("starting_angle_deg")
    if starting_angle_deg is None:
        starting_angle_deg = geom.starting_angle_deg
    starting_frame = choose("starting_frame")
    if starting_frame is None:
        starting_frame = geom.starting_frame
    oscillation_range_deg = choose("oscillation_range_deg")
    if oscillation_range_deg is None:
        oscillation_range_deg = geom.oscillation_range_deg

    nx = choose("nx")
    if nx is None:
        nx = geom.nx
    ny = choose("ny")
    if ny is None:
        ny = geom.ny
    qx_mm = choose("qx_mm")
    if qx_mm is None:
        qx_mm = geom.qx_mm
    qy_mm = choose("qy_mm")
    if qy_mm is None:
        qy_mm = geom.qy_mm
    orgx_px = choose("orgx_px")
    if orgx_px is None:
        orgx_px = geom.orgx_px
    orgy_px = choose("orgy_px")
    if orgy_px is None:
        orgy_px = geom.orgy_px
    detector_distance_mm = choose("detector_distance_mm")
    if detector_distance_mm is None:
        detector_distance_mm = geom.detector_distance_mm

    det_x = choose("det_x")
    if det_x is None:
        det_x = geom.det_x
    det_y = choose("det_y")
    if det_y is None:
        det_y = geom.det_y
    det_z = geom.det_z
    if "det_x" in ascii_data or "det_y" in ascii_data:
        dz = np.cross(det_x, det_y)
        n = np.linalg.norm(dz)
        if n > 0:
            det_z = dz / n

    a_axis_A = choose("a_axis_A")
    if a_axis_A is None:
        a_axis_A = geom.a_axis_A
    b_axis_A = choose("b_axis_A")
    if b_axis_A is None:
        b_axis_A = geom.b_axis_A
    c_axis_A = choose("c_axis_A")
    if c_axis_A is None:
        c_axis_A = geom.c_axis_A

    reflecting_range_esd = ascii_data.get("reflecting_range_esd_deg", None)
    beam_div_esd = ascii_data.get("beam_divergence_esd_deg", None)

    # Beam direction: GXPARM can store non-unit. If ASCII header provides unit, we can override direction.
    if "incident_beam_dir_unit" in ascii_data:
        incident_beam_dir = np.array(ascii_data["incident_beam_dir_unit"], dtype=float)
    else:
        incident_beam_dir = geom.incident_beam_dir

    return XDSGeometry(
        starting_frame=starting_frame,
        starting_angle_deg=starting_angle_deg,
        oscillation_range_deg=oscillation_range_deg,
        rotation_axis=rotation_axis,
        wavelength_A=geom.wavelength_A,
        incident_beam_dir=incident_beam_dir,
        space_group_number=geom.space_group_number,
        unit_cell_constants=geom.unit_cell_constants,
        a_axis_A=a_axis_A,
        b_axis_A=b_axis_A,
        c_axis_A=c_axis_A,
        nx=nx,
        ny=ny,
        qx_mm=qx_mm,
        qy_mm=qy_mm,
        orgx_px=orgx_px,
        orgy_px=orgy_px,
        detector_distance_mm=detector_distance_mm,
        det_x=det_x,
        det_y=det_y,
        det_z=det_z,
        name_template_of_data_frames=name_template,
        data_range=data_range,
        include_resolution_range=include_res,
        reflecting_range_esd_deg=reflecting_range_esd,
        beam_divergence_esd_deg=beam_div_esd,
    )
