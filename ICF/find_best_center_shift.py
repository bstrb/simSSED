import numpy as np
from compute_wedge_radial_profiles import compute_wedge_radial_profiles

def find_best_center_shift(image, mask, current_center, indices, step_size=1.0, n_steps=3,
                           n_wedges=8, n_rad_bins=200):
    """
    Search in a small grid around current_center to find the shift that 
    best matches opposite wedge radial profiles.
    
    Args:
        image (np.ndarray)
        mask (np.ndarray)
        current_center (tuple): (cx, cy)
        indices (tuple): Precomputed indices (y_indices, x_indices).
        step_size (float): Step in pixels for scanning around current center.
        n_steps (int): Number of steps in each direction.
                       e.g. if n_steps=3, test shifts in [-step_size, 0, +step_size].
        n_wedges (int)
        n_rad_bins (int)
    
    Returns:
        best_shift (tuple): (dx, dy) that best aligns opposite wedges.
    """
    # Define a function that quantifies "misalignment" for a given center.
    def misalignment_metric(test_center):
        # Pass the precomputed indices to compute_wedge_radial_profiles.
        wedge_profiles, _ = compute_wedge_radial_profiles(
            image, mask, test_center, indices,
            n_wedges=n_wedges, 
            n_rad_bins=n_rad_bins
        )
        # Compare wedge i with wedge i + n_wedges/2
        half = n_wedges // 2
        total_diff = 0.0
        count = 0
        for i in range(half):
            profile1 = wedge_profiles[i]
            profile2 = wedge_profiles[i + half]
            # Ignore NaNs:
            valid_mask = ~np.isnan(profile1) & ~np.isnan(profile2)
            if np.any(valid_mask):
                diff = profile1[valid_mask] - profile2[valid_mask]
                total_diff += np.sum(diff**2)  # Sum of squared differences.
                count += np.sum(valid_mask)
        if count > 0:
            return total_diff / count
        else:
            return np.inf
    
    cx, cy = current_center
    shift_options = np.linspace(-step_size, step_size, n_steps)
    
    best_dx = 0.0
    best_dy = 0.0
    best_misalign = np.inf
    
    for dx in shift_options:
        for dy in shift_options:
            test_center = (cx + dx, cy + dy)
            mis = misalignment_metric(test_center)
            if mis < best_misalign:
                best_misalign = mis
                best_dx = dx
                best_dy = dy
                
    return best_dx, best_dy
