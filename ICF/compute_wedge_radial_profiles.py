import numpy as np

def compute_wedge_radial_profiles(image, mask, center, indices, 
                                       n_wedges=8, n_rad_bins=200, r_max=None):
    """
    A faster, vectorized version of computing wedge profiles.
    Uses precomputed indices and np.digitize for radial binning.
    """
    y_indices, x_indices = indices
    cx, cy = center
    # Compute r and theta in a vectorized way.
    r = np.sqrt((y_indices - cx)**2 + (x_indices - cy)**2)
    theta = np.arctan2((y_indices - cx), (x_indices - cy))
    
    if r_max is None:
        r_max = min(image.shape) / 2.0
    r_edges = np.linspace(0, r_max, n_rad_bins+1)
    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    
    wedge_profiles = []
    wedge_step = 2*np.pi / n_wedges
    
    # Loop over wedges only (fewer iterations)
    for w in range(n_wedges):
        angle_min = -np.pi + w * wedge_step
        angle_max = -np.pi + (w+1) * wedge_step
        
        # Build a wedge mask using precomputed theta and the user mask.
        wedge_mask = (theta >= angle_min) & (theta < angle_max) & mask
        
        # Use np.digitize to assign each pixel in the wedge to a radial bin.
        bin_indices = np.digitize(r[wedge_mask], r_edges) - 1  # bins: 0 to n_rad_bins-1
        
        # Vectorized grouping is tricky for medians, but you can loop over bins (which is fewer iterations)
        profile = np.empty(n_rad_bins)
        wedge_vals = image[wedge_mask]
        for bin_i in range(n_rad_bins):
            vals = wedge_vals[bin_indices == bin_i]
            profile[bin_i] = np.median(vals) if vals.size > 0 else np.nan
        wedge_profiles.append(profile)
    
    return wedge_profiles, r_centers
