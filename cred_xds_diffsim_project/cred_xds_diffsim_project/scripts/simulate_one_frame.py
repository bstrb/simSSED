\
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import imageio.v2 as imageio

from cred_sim.xds import load_xds_geometry
from cred_sim.reflections import generate_hkls, intensity_model, default_s_max_from_xds_header
from cred_sim.simulation import SimulationParams, simulate_frame, render_pattern

def main():
    ap = argparse.ArgumentParser(description="Simulate a single diffraction frame from XDS geometry/orientations.")
    ap.add_argument("--xds", required=True, help="Path to XDS folder (must contain GXPARM.XDS)")
    ap.add_argument("--frame", type=int, required=True, help="Frame number (1-based, like XDS)")
    ap.add_argument("--out", required=True, help="Output PNG (or .npy)")
    ap.add_argument("--dmin", type=float, default=None, help="d_min (Å). Default: from XDS_ASCII.HKL header if available else 1.0")
    ap.add_argument("--dmax", type=float, default=None, help="d_max (Å) low-res cutoff (optional). Default: from XDS header if available")
    ap.add_argument("--smax", type=float, default=None, help="Ewald proximity tolerance (1/Å). Default: heuristic from XDS header if possible else 0.002")
    ap.add_argument("--sigma", type=float, default=1.2, help="Spot sigma (px) for Gaussian blur")
    ap.add_argument("--background", type=float, default=0.0, help="Background level")
    ap.add_argument("--noise", type=float, default=0.0, help="Gaussian noise sigma")
    ap.add_argument("--intensity-model", default="constant",
                    choices=["constant","lorentz_like","from_cif_electron","from_cif_xray"])
    ap.add_argument("--cif", default=None, help="Optional CIF for structure factors (needed for from_cif_* intensity models)")
    ap.add_argument("--orientation-reference", default="phi0", choices=["phi0","frame0"],
                    help="How to interpret the reference orientation in GXPARM/XDS header")
    ap.add_argument("--save-spots", default=None, help="Optional CSV path to save predicted spot list")
    args = ap.parse_args()

    xds_dir = Path(args.xds)
    geom = load_xds_geometry(xds_dir)

    # Defaults from XDS header if present
    dmin = args.dmin
    dmax = args.dmax
    if geom.include_resolution_range is not None:
        # XDS stores (dmax, dmin)
        dmax_hdr, dmin_hdr = geom.include_resolution_range
        if dmin is None:
            dmin = float(dmin_hdr)
        if dmax is None:
            dmax = float(dmax_hdr)
    if dmin is None:
        dmin = 1.0

    smax = args.smax
    if smax is None:
        smax = default_s_max_from_xds_header(geom)
    if smax is None:
        smax = 0.002

    hkls = generate_hkls(geom, d_min_A=dmin, d_max_A=dmax, include_friedel=True)

    I = intensity_model(geom, hkls, model=args.intensity_model, cif_path=args.cif,
                        cache_path=(xds_dir/"_cache"/f"I_{args.intensity_model}_dmin{dmin:.3f}.npz") if args.cif else None)

    params = SimulationParams(
        d_min_A=dmin,
        d_max_A=dmax,
        s_max_invA=float(smax),
        spot_sigma_px=float(args.sigma),
        background=float(args.background),
        noise_sigma=float(args.noise),
        intensity_scale=1.0,
        orientation_reference=args.orientation_reference,
    )

    spots = simulate_frame(geom, frame=args.frame, hkls=hkls, hkl_intensity=I, params=params)
    img = render_pattern(geom, spots, params=params)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() == ".npy":
        np.save(out, img)
    else:
        # normalize to uint16 for PNG
        im = img - img.min()
        if im.max() > 0:
            im = im / im.max()
        im16 = np.clip(im * 65535.0, 0, 65535).astype(np.uint16)
        imageio.imwrite(out, im16)

    if args.save_spots:
        Path(args.save_spots).parent.mkdir(parents=True, exist_ok=True)
        spots.to_csv(args.save_spots, index=False)

    print(f"Simulated frame {args.frame} -> {out}")
    print(f"Spots: {len(spots)}  dmin={dmin}Å  dmax={dmax}Å  smax={smax}  sigma={args.sigma}px")

if __name__ == "__main__":
    main()
