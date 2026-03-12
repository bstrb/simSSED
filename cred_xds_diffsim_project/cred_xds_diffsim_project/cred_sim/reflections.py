\
"""
Reflection list generation + optional structure-factor intensity models.

- generate_hkls(): produce a list of (h,k,l) within a resolution cutoff
- intensity_from_cif(): compute kinematic |F|^2 from a CIF using gemmi's
  StructureFactorCalculatorE (electron) or X (x-ray) as an optional step.

This is intentionally simple and meant as a baseline.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Literal, Dict

import numpy as np

from .xds import XDSGeometry

IntensityModel = Literal["constant", "lorentz_like", "from_cif_electron", "from_cif_xray"]

def generate_hkls(geom: XDSGeometry,
                  d_min_A: float,
                  d_max_A: Optional[float] = None,
                  hkl_max: Optional[int] = None,
                  include_friedel: bool = True) -> np.ndarray:
    """
    Generate integer hkls with d-spacing between [d_min, d_max] (Å).

    Uses reciprocal basis from geom (no 2π convention), so:
        |g| = 1 / d

    This function does NOT enforce systematic absences (kept minimal by design).

    Parameters
    ----------
    d_min_A : float
        Minimum d-spacing (highest resolution).
    d_max_A : Optional[float]
        Maximum d-spacing (lowest resolution). If None, includes down to 1/|g| -> inf
        but we always exclude (0,0,0).
    hkl_max : Optional[int]
        If provided, use [-hkl_max, hkl_max] for each axis. Otherwise choose a conservative bound.
    include_friedel : bool
        If False, keep only one of (h,k,l) and (-h,-k,-l) for non-centrosymmetric patterns.
        Default True.
    """
    if d_min_A <= 0:
        raise ValueError("d_min_A must be > 0")

    # Conservative hkl bound based on cell lengths.
    a, b, c, *_ = geom.unit_cell_constants
    if hkl_max is None:
        # For orthogonal-ish cells, max index roughly a/d_min etc.
        hkl_max = int(np.ceil(max(a, b, c) / d_min_A)) + 1

    # Generate grid
    rng = np.arange(-hkl_max, hkl_max + 1, dtype=int)
    H, K, L = np.meshgrid(rng, rng, rng, indexing="ij")
    hkls = np.stack([H.ravel(), K.ravel(), L.ravel()], axis=1)

    # Drop 0,0,0
    hkls = hkls[np.any(hkls != 0, axis=1)]

    # Resolution filter using reciprocal basis at reference orientation
    B = geom.reciprocal_basis_invA()  # columns a*, b*, c*
    g = hkls @ B.T  # (N,3) because row vector * (3x3)^T

    gnorm = np.linalg.norm(g, axis=1)
    # d = 1/|g|
    d = np.where(gnorm > 0, 1.0 / gnorm, np.inf)

    mask = d >= d_min_A  # NOTE: for d-spacing, smaller d = higher res.
    # Actually want d between [d_min, d_max]; so require d >= d_min? Wait:
    # d_min is minimum d spacing (small). So keep d >= d_min? That would keep *low-res*.
    # Correct is: keep d >= d_min? No, if d_min=0.6, we want d >= 0.6 (0.6..inf) -> includes all LOWER resolution too.
    # But we also want to cap at d_max (e.g., 20 Å). So set d <= d_max to remove very low res.
    # So:
    mask = d >= d_min_A
    if d_max_A is not None:
        mask &= d <= d_max_A

    hkls = hkls[mask]

    if not include_friedel:
        # Keep a unique representative by enforcing a lexicographic sign convention.
        # Simple rule: first non-zero index positive.
        def key(hkl):
            for x in hkl:
                if x != 0:
                    return x > 0
            return True
        keep = []
        seen = set()
        for h,k,l in hkls:
            if (h,k,l) in seen or (-h,-k,-l) in seen:
                continue
            if key((h,k,l)):
                keep.append((h,k,l))
                seen.add((h,k,l))
            else:
                keep.append((-h,-k,-l))
                seen.add((-h,-k,-l))
        hkls = np.array(keep, dtype=int)

    return hkls

def default_s_max_from_xds_header(geom: XDSGeometry) -> Optional[float]:
    """
    If reflecting range E.S.D. is present (degrees), make a conservative excitation
    tolerance estimate in 1/Å.

    This is a *heuristic* mapping and is not an XDS-equivalent partiality model.

    Returns None if required header values are missing.
    """
    if geom.reflecting_range_esd_deg is None:
        return None
    # Convert angular width to reciprocal-space tolerance.
    # For small angles, delta_theta ~ |g|/|k|, but we need a tolerance independent of g.
    # We instead map angular sigma to a delta in |k| direction: s_max ≈ |k| * sigma_theta.
    # k = 1/λ (1/Å)
    k = 1.0 / geom.wavelength_A
    sigma_theta = np.deg2rad(geom.reflecting_range_esd_deg)
    return float(k * sigma_theta)

def intensity_model(geom: XDSGeometry,
                    hkls: np.ndarray,
                    model: IntensityModel = "constant",
                    cif_path: Optional[str | Path] = None,
                    cache_path: Optional[str | Path] = None) -> np.ndarray:
    """
    Return per-hkl relative intensities.

    - constant: all 1
    - lorentz_like: 1/(|g|^2 + eps) as a toy model
    - from_cif_electron: uses gemmi.StructureFactorCalculatorE
    - from_cif_xray: uses gemmi.StructureFactorCalculatorX

    Intensities are normalized to max=1 (unless all zeros).
    """
    hkls = np.asarray(hkls, dtype=int)
    if model == "constant":
        return np.ones(len(hkls), dtype=float)

    # Reciprocal length for toy scaling
    B = geom.reciprocal_basis_invA()
    g = hkls @ B.T
    g2 = np.sum(g*g, axis=1)

    if model == "lorentz_like":
        eps = 1e-6
        I = 1.0 / (g2 + eps)
        I = I / np.max(I)
        return I.astype(float)

    if model in ("from_cif_electron", "from_cif_xray"):
        if cif_path is None:
            raise ValueError(f"cif_path is required for intensity model {model}")

        # Cache to speed up repeated runs
        if cache_path is not None:
            cache_path = Path(cache_path)
            if cache_path.exists():
                arr = np.load(cache_path)
                if "I" in arr and "hkls" in arr:
                    if np.array_equal(arr["hkls"], hkls):
                        return arr["I"].astype(float)

        import gemmi

        cif_path = Path(cif_path)
        # Try small structure first (common for small molecules/MOFs).
        ss = None
        st = None
        try:
            ss = gemmi.read_small_structure(str(cif_path))
        except Exception:
            ss = None
        if ss is None:
            st = gemmi.read_structure(str(cif_path))

        if ss is not None:
            cell = ss.cell
        else:
            cell = st.cell

        if model == "from_cif_electron":
            calc = gemmi.StructureFactorCalculatorE(cell)
        else:
            calc = gemmi.StructureFactorCalculatorX(cell)

        I = np.zeros(len(hkls), dtype=float)
        if ss is not None:
            for i, (h,k,l) in enumerate(hkls):
                F = calc.calculate_sf_from_small_structure(ss, (int(h), int(k), int(l)))
                I[i] = (F.real*F.real + F.imag*F.imag)
        else:
            # Use the first model by default
            mdl = st[0]
            for i, (h,k,l) in enumerate(hkls):
                F = calc.calculate_sf_from_model(mdl, (int(h), int(k), int(l)))
                I[i] = (F.real*F.real + F.imag*F.imag)

        # Normalize
        m = float(np.max(I)) if len(I) else 1.0
        if m > 0:
            I = I / m

        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(cache_path, hkls=hkls, I=I)

        return I.astype(float)

    raise ValueError(f"Unknown intensity model: {model}")
