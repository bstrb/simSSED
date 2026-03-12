# cRED diffraction simulation from XDS orientations (minimal parser)

This is a small, self-contained Python project that:

1. **Parses only the geometry + orientation state needed** from an XDS folder:
   - `GXPARM.XDS` (classic `XPARM.XDS` fixed-format block)
   - (optional) `XDS.INP` for `NAME_TEMPLATE_OF_DATA_FRAMES` and `DATA_RANGE` if you want to load experimental frames

2. Builds a per-frame orientation model using the XDS rotation axis and oscillation range.

3. Simulates **spot positions** (and optional toy intensities) on the detector for any selected frames.

4. Lets you “turn knobs” (resolution cutoff, excitation error tolerance, spot sigma, background/noise, intensity model).

## What this does NOT do
- It does **not** parse `INTEGRATE.HKL`, `XDS_ASCII.HKL`, `CORRECT.LP`, or the `.cbf` correction images (unless you explicitly choose to).
- It does **not** do dynamical scattering. This is a kinematic/geometry simulator intended for *orientation/geometry sanity-checking* and for building a baseline that you can extend.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run a quick single-frame simulation:

```bash
python scripts/simulate_one_frame.py --xds example_xds --frame 1 --out out/frame_0001.png
```

Open the notebook:

```bash
jupyter lab notebooks/01_simulate_from_xds.ipynb
```

## Knobs you can turn

- `d_min_A`: resolution cutoff (Å)
- `s_max_invA`: excitation error tolerance (1/Å) controlling which reflections are considered “excited”
- `spot_sigma_px`: spot blur in pixels
- `intensity_model`: `constant` or `lorentz_like` or `from_cif_xray` (optional CIF, x-ray SFs only; placeholder for electron SFs)
- `background`, `noise_sigma`

## Notes on coordinate system
This project follows the *XDS laboratory frame* convention where (in the common/default setup) the
detector x/y axes are the lab x/y axes and the beam points along +z (as in your `XDS.INP`).

If your dataset uses a different detector axis definition, `GXPARM.XDS` includes those axes and they
are honored automatically.

---

If you want, I can adapt the simulator to:
- read your actual **SMV / MRC / TIFF** frames,
- estimate a better excitation model (mosaicity / thickness),
- or compute intensities using a CIF with *electron* scattering factors (needs extra tables or a library).
