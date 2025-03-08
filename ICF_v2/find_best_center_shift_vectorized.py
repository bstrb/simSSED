# find_best_center_shift_vectorized.py
import numpy as np
from compute_wedge_radial_profiles_shifted import compute_wedge_radial_profiles_shifted

def find_best_center_shift_vectorized(image, mask, current_center, base_center, dx_base, dy_base,
                                      step_size=1.0, n_steps=3, n_wedges=8, n_rad_bins=200):
    # Create a grid of candidate shifts (in pixels).
    shift_vals = np.linspace(-step_size, step_size, n_steps)
    DX, DY = np.meshgrid(shift_vals, shift_vals)
    candidate_shifts = np.column_stack((DY.ravel(), DX.ravel()))  # (delta_y, delta_x)
    
    best_shift = None
    best_metric = np.inf
    
    # Current offset relative to base_center.
    current_offset = (current_center[0] - base_center[0], current_center[1] - base_center[1])
    # print(f"[DEBUG] Current offset: {current_offset}")
    
    for candidate in candidate_shifts:
        # Effective shift = current_offset + candidate.
        effective_shift = (current_offset[0] + candidate[0], current_offset[1] + candidate[1])
        wedge_profiles, _ = compute_wedge_radial_profiles_shifted(
            image, mask, base_center, effective_shift, dx_base, dy_base,
            n_wedges=n_wedges, n_rad_bins=n_rad_bins
        )
        # Compute misalignment metric between opposite wedges.
        half = n_wedges // 2
        total_diff = 0.0
        count = 0
        for i in range(half):
            p1 = wedge_profiles[i]
            p2 = wedge_profiles[i + half]
            valid = ~np.isnan(p1) & ~np.isnan(p2)
            if np.any(valid):
                diff = p1[valid] - p2[valid]
                total_diff += np.sum(diff**2)
                count += np.sum(valid)
        metric = total_diff / count if count > 0 else np.inf
        # Print candidate and its metric.
        # print(f"[DEBUG] Candidate shift: {candidate}, Metric: {metric:.4e}")
        if metric < best_metric:
            best_metric = metric
            best_shift = candidate
            
    # print(f"[DEBUG] Best candidate shift selected: {best_shift} with metric: {best_metric:.4e}")
    return best_shift
