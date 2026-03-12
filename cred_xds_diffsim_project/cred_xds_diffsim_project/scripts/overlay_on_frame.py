\
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from cred_sim.xds import load_xds_geometry
from cred_sim.io import read_image
from cred_sim.reflections import generate_hkls, intensity_model, default_s_max_from_xds_header
from cred_sim.simulation import SimulationParams, simulate_frame
from cred_sim.plotting import overlay_spots

def main():
    ap = argparse.ArgumentParser(description="Overlay predicted spots on an experimental image.")
    ap.add_argument("--xds", required=True, help="Path to XDS folder")
    ap.add_argument("--frame", type=int, required=True, help="Frame number (1-based)")
    ap.add_argument("--image", required=True, help="Experimental frame path (SMV .img, MRC, png/tif via imageio)")
    ap.add_argument("--dmin", type=float, default=None)
    ap.add_argument("--dmax", type=float, default=None)
    ap.add_argument("--smax", type=float, default=None)
    ap.add_argument("--intensity-model", default="constant",
                    choices=["constant","lorentz_like","from_cif_electron","from_cif_xray"])
    ap.add_argument("--cif", default=None)
    ap.add_argument("--orientation-reference", default="phi0", choices=["phi0","frame0"])
    ap.add_argument("--out", default=None, help="Optional output PNG for the overlay")
    args = ap.parse_args()

    geom = load_xds_geometry(args.xds)

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
                        cache_path=(Path(args.xds)/"_cache"/f"I_{args.intensity_model}_dmin{dmin:.3f}.npz") if args.cif else None)

    params = SimulationParams(d_min_A=dmin, d_max_A=dmax, s_max_invA=float(smax),
                              orientation_reference=args.orientation_reference)

    spots = simulate_frame(geom, frame=args.frame, hkls=hkls, hkl_intensity=I, params=params)
    img = read_image(args.image)

    overlay_spots(img, spots, title=f"Frame {args.frame} overlay (spots={len(spots)})")
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.out, dpi=200)
        print(f"Saved overlay -> {args.out}")
    else:
        plt.show()

if __name__ == "__main__":
    main()
