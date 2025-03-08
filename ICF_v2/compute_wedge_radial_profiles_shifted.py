# import numpy as np
# from compute_bin_medians import compute_bin_medians

# def compute_wedge_radial_profiles_shifted(image, mask, base_center, shift, dx_base, dy_base, 
#                                           n_wedges=8, n_rad_bins=200, r_max=None):
#     """
#     Compute wedge profiles using precomputed dx_base and dy_base.
#     shift: tuple (delta_y, delta_x) to adjust from base_center.
#     """
#     # Compute the new effective differences.
#     dy = dy_base - shift[0]
#     dx = dx_base - shift[1]
#     r = np.sqrt(dy**2 + dx**2)
#     theta = np.arctan2(dy, dx)
    
#     if r_max is None:
#         r_max = min(image.shape) / 2.0
#     r_edges = np.linspace(0, r_max, n_rad_bins+1)
    
#     wedge_profiles = []
#     wedge_step = 2 * np.pi / n_wedges
    
#     for w in range(n_wedges):
#         angle_min = -np.pi + w * wedge_step
#         angle_max = -np.pi + (w+1) * wedge_step
        
#         wedge_mask = (theta >= angle_min) & (theta < angle_max) & mask
#         bin_indices = np.digitize(r[wedge_mask], r_edges) - 1
#         wedge_vals = image[wedge_mask]
#         profile = compute_bin_medians(wedge_vals, bin_indices, n_rad_bins)
#         wedge_profiles.append(profile)
        
#     # Also compute radial bin centers.
#     r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
#     return wedge_profiles, r_centers

# compute_wedge_radial_profiles_shifted.py
import numpy as np
from compute_bin_medians import compute_bin_medians  # your Numba-accelerated function

def compute_wedge_radial_profiles_shifted(image, mask, base_center, shift, dx_base, dy_base,
                                          n_wedges=8, n_rad_bins=200, r_max=None,
                                          max_intensity=None):
    """
    Compute wedge profiles using precomputed dx_base and dy_base.
    
    Parameters:
        image (np.ndarray): 2D image array.
        mask (np.ndarray): Boolean mask array.
        base_center (tuple): The center used to precompute dx_base, dy_base.
        shift (tuple): (delta_y, delta_x) so that effective center = base_center + shift.
        dx_base (np.ndarray): Precomputed column differences.
        dy_base (np.ndarray): Precomputed row differences.
        n_wedges (int): Number of angular wedges.
        n_rad_bins (int): Number of radial bins.
        r_max (float): Maximum radius to consider.
        max_intensity (float or None): If set, pixels with intensity greater than this value
                                       will be excluded from the median computation.
        
    Returns:
        wedge_profiles (list of np.ndarray): The median profile per wedge.
        r_centers (np.ndarray): Radial bin centers.
    """
    # Compute effective differences.
    new_dy = dy_base - shift[0]
    new_dx = dx_base - shift[1]
    r = np.sqrt(new_dy**2 + new_dx**2)
    theta = np.arctan2(new_dy, new_dx)
    
    if r_max is None:
        r_max = min(image.shape) / 2.0
    r_edges = np.linspace(0, r_max, n_rad_bins+1)
    
    wedge_profiles = []
    wedge_step = 2 * np.pi / n_wedges
    
    for w in range(n_wedges):
        angle_min = -np.pi + w * wedge_step
        angle_max = -np.pi + (w+1) * wedge_step
        
        wedge_mask = (theta >= angle_min) & (theta < angle_max) & mask
        # Get radial distances and intensities for this wedge.
        r_wedge = r[wedge_mask]
        wedge_vals = image[wedge_mask]
        
        # If max_intensity is set, filter out the highest intensities.
        if max_intensity is not None:
            valid = wedge_vals < max_intensity
            r_wedge = r_wedge[valid]
            wedge_vals = wedge_vals[valid]
        
        # Bin the radial distances.
        bin_indices = np.digitize(r_wedge, r_edges) - 1  # bins: 0 to n_rad_bins-1
        # Compute median for each bin.
        profile = compute_bin_medians(wedge_vals, bin_indices, n_rad_bins)
        wedge_profiles.append(profile)
        
    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    return wedge_profiles, r_centers
