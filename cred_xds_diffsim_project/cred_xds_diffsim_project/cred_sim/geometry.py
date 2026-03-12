\
"""
Geometry helpers: rotations, mapping between lab <-> detector, etc.
"""
from __future__ import annotations

import numpy as np

def rotation_matrix(axis: np.ndarray, angle_rad: float) -> np.ndarray:
    """
    Rodrigues rotation formula.
    axis: (3,) unit or non-unit; will be normalized.
    """
    axis = np.asarray(axis, dtype=float)
    n = np.linalg.norm(axis)
    if n == 0:
        raise ValueError("Rotation axis has zero length")
    x, y, z = axis / n
    c = float(np.cos(angle_rad))
    s = float(np.sin(angle_rad))
    C = 1.0 - c
    R = np.array([
        [c + x*x*C,     x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s,   c + y*y*C,   y*z*C - x*s],
        [z*x*C - y*s,   z*y*C + x*s, c + z*z*C],
    ], dtype=float)
    return R

def spindle_angle_deg(starting_angle_deg: float, oscillation_range_deg: float, starting_frame: int, frame: int) -> float:
    return float(starting_angle_deg + oscillation_range_deg * (frame - starting_frame))

def scatter_to_detector_xy_mm(ray_dir: np.ndarray,
                             det_x: np.ndarray,
                             det_y: np.ndarray,
                             det_z: np.ndarray,
                             distance_mm: float,
                             beam_dir_unit: np.ndarray) -> tuple[float, float]:
    """
    Map a unit ray direction (in lab frame) to detector x/y in mm relative to the direct beam point.

    The detector plane is defined by normal det_z and is positioned at distance_mm along det_z
    from the origin (crystal).

    We compute intersection point p = (distance / dot(ray, det_z)) * ray.
    Then subtract p0 (direct beam intersection) so that beam hits (0,0).
    Finally project onto det_x/det_y to get (x_mm,y_mm).

    This remains valid if the beam is slightly tilted relative to det_z.
    """
    ray_dir = np.asarray(ray_dir, dtype=float)
    det_x = np.asarray(det_x, dtype=float)
    det_y = np.asarray(det_y, dtype=float)
    det_z = np.asarray(det_z, dtype=float)
    beam_dir_unit = np.asarray(beam_dir_unit, dtype=float)

    denom = float(np.dot(ray_dir, det_z))
    if denom <= 0:
        # Ray points away from detector plane
        return (np.nan, np.nan)
    p = (distance_mm / denom) * ray_dir

    denom0 = float(np.dot(beam_dir_unit, det_z))
    if denom0 <= 0:
        raise ValueError("Beam direction does not intersect detector plane with positive distance")
    p0 = (distance_mm / denom0) * beam_dir_unit

    dp = p - p0
    x_mm = float(np.dot(dp, det_x))
    y_mm = float(np.dot(dp, det_y))
    return x_mm, y_mm

def mm_to_pixel(x_mm: float, y_mm: float, orgx_px: float, orgy_px: float, qx_mm: float, qy_mm: float) -> tuple[float, float]:
    x_px = orgx_px + (x_mm / qx_mm)
    y_px = orgy_px + (y_mm / qy_mm)
    return float(x_px), float(y_px)
