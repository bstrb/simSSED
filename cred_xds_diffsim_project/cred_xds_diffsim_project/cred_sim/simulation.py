\
"""
Core diffraction simulation.

This is a geometry/kinematic simulator:
- Compute g vectors for hkls at a given frame orientation
- Apply an Ewald-sphere proximity criterion to decide "excited" reflections
- Map excited reflections to detector pixel coordinates
- Render a synthetic pattern image
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter

from .xds import XDSGeometry
from .geometry import rotation_matrix, spindle_angle_deg, scatter_to_detector_xy_mm, mm_to_pixel

@dataclass(frozen=True)
class SimulationParams:
    d_min_A: float = 1.0
    d_max_A: Optional[float] = None
    s_max_invA: float = 0.002  # Ewald proximity tolerance (1/Å)
    spot_sigma_px: float = 1.2
    background: float = 0.0
    noise_sigma: float = 0.0
    intensity_scale: float = 1.0
    # How to interpret the reference orientation:
    # - "phi0": axes are defined at spindle angle 0°, then rotate by phi(frame)
    # - "frame0": axes are defined at STARTING_FRAME, then rotate by (frame-start) * osc_range
    orientation_reference: str = "phi0"  # "phi0" or "frame0"

def _frame_rotation(geom: XDSGeometry, frame: int, orientation_reference: str) -> np.ndarray:
    axis = geom.rotation_axis_unit()
    if orientation_reference == "phi0":
        phi_deg = spindle_angle_deg(geom.starting_angle_deg, geom.oscillation_range_deg, geom.starting_frame, frame)
        ang = np.deg2rad(phi_deg)
    elif orientation_reference == "frame0":
        # relative to the starting frame
        dphi_deg = geom.oscillation_range_deg * (frame - geom.starting_frame)
        ang = np.deg2rad(dphi_deg)
    else:
        raise ValueError("orientation_reference must be 'phi0' or 'frame0'")
    return rotation_matrix(axis, ang)

def simulate_frame(geom: XDSGeometry,
                   frame: int,
                   hkls: np.ndarray,
                   hkl_intensity: Optional[np.ndarray] = None,
                   params: Optional[SimulationParams] = None) -> pd.DataFrame:
    """
    Simulate which reflections are excited at a given frame and where they land on the detector.

    Returns a DataFrame with columns:
      h,k,l, x_px, y_px, I_rel, delta_k (Ewald proximity), gnorm
    """
    if params is None:
        params = SimulationParams()

    hkls = np.asarray(hkls, dtype=int)
    if hkls.ndim != 2 or hkls.shape[1] != 3:
        raise ValueError("hkls must be (N,3) int array")
    N = hkls.shape[0]

    if hkl_intensity is None:
        I0 = np.ones(N, dtype=float)
    else:
        I0 = np.asarray(hkl_intensity, dtype=float)
        if I0.shape != (N,):
            raise ValueError("hkl_intensity must have same length as hkls")

    # Reference reciprocal basis
    B0 = geom.reciprocal_basis_invA()  # columns
    g0 = hkls @ B0.T  # (N,3) in lab at reference orientation

    # Rotate to this frame
    R = _frame_rotation(geom, frame, params.orientation_reference)
    g = (R @ g0.T).T  # (N,3)

    # Incident wavevector magnitude
    lam = geom.wavelength_A
    k = 1.0 / lam
    beam_dir = geom.beam_dir_unit()
    k0 = beam_dir * k

    kout = g + k0[None, :]
    kout_norm = np.linalg.norm(kout, axis=1)

    # Ewald proximity
    delta = kout_norm - k  # (1/Å)
    mask = np.abs(delta) <= params.s_max_invA

    if not np.any(mask):
        return pd.DataFrame(columns=["h","k","l","x_px","y_px","I_rel","delta_k","gnorm"])

    hkls_sel = hkls[mask]
    g_sel = g[mask]
    I_sel = I0[mask]

    kout_sel = kout[mask]
    koutn_sel = kout_norm[mask]
    ray_dir = kout_sel / koutn_sel[:, None]  # unit vector

    # Map to detector
    x_mm = np.empty(len(hkls_sel), dtype=float)
    y_mm = np.empty(len(hkls_sel), dtype=float)
    for i, r in enumerate(ray_dir):
        xm, ym = scatter_to_detector_xy_mm(r, geom.det_x, geom.det_y, geom.det_z,
                                           geom.detector_distance_mm, beam_dir)
        x_mm[i] = xm
        y_mm[i] = ym

    x_px = np.empty(len(hkls_sel), dtype=float)
    y_px = np.empty(len(hkls_sel), dtype=float)
    for i, (xm, ym) in enumerate(zip(x_mm, y_mm)):
        xp, yp = mm_to_pixel(xm, ym, geom.orgx_px, geom.orgy_px, geom.qx_mm, geom.qy_mm)
        x_px[i] = xp
        y_px[i] = yp

    # Filter to detector bounds (+ a margin)
    margin = 10.0
    in_bounds = (x_px >= -margin) & (x_px <= geom.nx + margin) & (y_px >= -margin) & (y_px <= geom.ny + margin)
    hkls_sel = hkls_sel[in_bounds]
    g_sel = g_sel[in_bounds]
    I_sel = I_sel[in_bounds]
    x_px = x_px[in_bounds]
    y_px = y_px[in_bounds]
    delta_sel = delta[mask][in_bounds]
    gnorm = np.linalg.norm(g_sel, axis=1)

    # Scale intensities
    I_rel = (I_sel * float(params.intensity_scale)).astype(float)

    df = pd.DataFrame({
        "h": hkls_sel[:,0].astype(int),
        "k": hkls_sel[:,1].astype(int),
        "l": hkls_sel[:,2].astype(int),
        "x_px": x_px,
        "y_px": y_px,
        "I_rel": I_rel,
        "delta_k": delta_sel.astype(float),
        "gnorm": gnorm.astype(float),
    })
    return df

def render_pattern(geom: XDSGeometry,
                   spots: pd.DataFrame,
                   params: Optional[SimulationParams] = None,
                   dtype=np.float32) -> np.ndarray:
    """
    Render a diffraction pattern image given spot list.
    """
    if params is None:
        params = SimulationParams()

    img = np.zeros((geom.ny, geom.nx), dtype=np.float32)

    if len(spots) == 0:
        if params.background != 0:
            img += float(params.background)
        if params.noise_sigma != 0:
            img += np.random.normal(0.0, float(params.noise_sigma), size=img.shape).astype(np.float32)
        return img.astype(dtype)

    # Deposit intensities at nearest pixels
    xs = spots["x_px"].to_numpy(dtype=float)
    ys = spots["y_px"].to_numpy(dtype=float)
    Is = spots["I_rel"].to_numpy(dtype=float)

    xi = np.rint(xs).astype(int)
    yi = np.rint(ys).astype(int)

    valid = (xi >= 0) & (xi < geom.nx) & (yi >= 0) & (yi < geom.ny)
    xi = xi[valid]
    yi = yi[valid]
    Is = Is[valid]

    # Accumulate (handles multiple reflections mapping to same pixel)
    np.add.at(img, (yi, xi), Is.astype(np.float32))

    # Blur to spot size
    if params.spot_sigma_px and params.spot_sigma_px > 0:
        img = gaussian_filter(img, sigma=float(params.spot_sigma_px), mode="constant")

    # Add background and noise
    if params.background != 0:
        img += float(params.background)
    if params.noise_sigma != 0:
        img += np.random.normal(0.0, float(params.noise_sigma), size=img.shape).astype(np.float32)

    return img.astype(dtype)
