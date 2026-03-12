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
    ap = argparse.ArgumentParser(description="Simulate a range of frames and write PNGs and/or spot lists.")
    ap.add_argument("--xds", required=True, help="Path to XDS folder")
    ap.add_argument("--frames", nargs=2, type=int, required=True, metavar=("START","END"),
                    help="Frame range inclusive, e.g. --frames 1 50")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--stride", type=int, default=1, help="Simulate every Nth frame")
    ap.add_argument("--dmin", type=float, default=None)
    ap.add_argument("--dmax", type=float, default=None)
    ap.add_argument("--smax", type=float, default=None)
    ap.add_argument("--sigma", type=float, default=1.2)
    ap.add_argument("--background", type=float, default=0.0)
    ap.add_argument("--noise", type=float, default=0.0)
    ap.add_argument("--intensity-model", default="constant",
                    choices=["constant","lorentz_like","from_cif_electron","from_cif_xray"])
    ap.add_argument("--cif", default=None)
    ap.add_argument("--orientation-reference", default="phi0", choices=["phi0","frame0"])
    ap.add_argument("--save-spots-csv", action="store_true", help="Also save per-frame spot list CSVs")
    args = ap.parse_args()

    xds_dir = Path(args.xds)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    geom = load_xds_geometry(xds_dir)

    # Defaults from XDS header if present
    dmin = args.dmin
    dmax = args.dmax
    if geom.include_resolution_range is not None:
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

    start, end = args.frames
    for frame in range(start, end+1, args.stride):
        spots = simulate_frame(geom, frame=frame, hkls=hkls, hkl_intensity=I, params=params)
        img = render_pattern(geom, spots, params=params)

        # Save
        im = img - img.min()
        if im.max() > 0:
            im = im / im.max()
        im16 = np.clip(im * 65535.0, 0, 65535).astype(np.uint16)
        png_path = outdir / f"frame_{frame:04d}.png"
        imageio.imwrite(png_path, im16)

        if args.save_spots_csv:
            csv_path = outdir / f"frame_{frame:04d}_spots.csv"
            spots.to_csv(csv_path, index=False)

        print(f"Frame {frame:4d}: spots={len(spots)} -> {png_path}")

if __name__ == "__main__":
    main()
