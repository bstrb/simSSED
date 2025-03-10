# ICFTOTAL.py

import h5py
import numpy as np
import numba

@numba.njit
def compute_bin_medians(wedge_vals, bin_indices, n_bins):
    # Force output array to be float64 so we can represent NaN.
    result = np.empty(n_bins, dtype=np.float64)
    for bin_i in range(n_bins):
        count = 0
        for j in range(wedge_vals.shape[0]):
            if bin_indices[j] == bin_i:
                count += 1
        if count == 0:
            result[bin_i] = np.nan
        else:
            # Use float64 for temporary array as well.
            tmp = np.empty(count, dtype=np.float64)
            k = 0
            for j in range(wedge_vals.shape[0]):
                if bin_indices[j] == bin_i:
                    tmp[k] = wedge_vals[j]
                    k += 1
            tmp.sort()
            if count % 2 == 1:
                result[bin_i] = tmp[count // 2]
            else:
                result[bin_i] = 0.5 * (tmp[count // 2 - 1] + tmp[count // 2])
    return result

def compute_wedge_radial_profiles_shifted(image, mask, base_center, shift, dx_base, dy_base,
                                          n_wedges=8, n_rad_bins=200, r_max=None):
    """
    Compute wedge profiles using precomputed dx_base and dy_base.
    
    Parameters:
        image (np.ndarray): 2D image array.
        mask (np.ndarray): Boolean mask array.
        base_center (tuple): The center used to precompute dx_base and dy_base (in (x, y) order).
        shift (tuple): (delta_x, delta_y) so that the effective center = base_center + shift.
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
    # Compute effective differences using the (delta_x, delta_y) order.
    new_dx = dx_base - shift[0]
    new_dy = dy_base - shift[1]
    r = np.sqrt(new_dx**2 + new_dy**2)
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
        
        # Bin the radial distances.
        bin_indices = np.digitize(r_wedge, r_edges) - 1  # bins: 0 to n_rad_bins-1
        # Compute median for each bin.
        profile = compute_bin_medians(wedge_vals, bin_indices, n_rad_bins)
        wedge_profiles.append(profile)
        
    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    return wedge_profiles, r_centers


def center_of_mass_initial_guess(image, mask):
    """
    Compute a rough center-of-mass (CoM) for the image using valid pixels only.
    This will serve as our initial guess for the diffraction center.
    
    Args:
        image (np.ndarray): 2D array of intensities
        mask (np.ndarray): 2D array of booleans, True=valid, False=invalid
    
    Returns:
        (cx, cy): tuple of floats representing the (row, col) center guess
    """
    # Weighted by intensity, ignoring masked pixels
    # row indices, col indices
    rows, cols = np.indices(image.shape)
    
    valid_intensity = image[mask]
    valid_rows = rows[mask]
    valid_cols = cols[mask]
    
    total_intensity = np.sum(valid_intensity)
    if total_intensity == 0:
        # fallback in case your data is empty or something unexpected
        return (image.shape[0] / 2.0, image.shape[1] / 2.0)
    
    cx = np.sum(valid_cols * valid_intensity) / total_intensity
    cy = np.sum(valid_rows * valid_intensity) / total_intensity
    return (cx, cy)

def find_best_center_shift_vectorized(image, mask, current_center, base_center, dx_base, dy_base,
                                      step_size=1.0, n_steps=3, n_wedges=4, n_rad_bins=100):
    # Create a grid of candidate shifts (in pixels).
    shift_vals = np.linspace(-step_size, step_size, n_steps)
    DX, DY = np.meshgrid(shift_vals, shift_vals)
    # Now candidate_shifts is in (delta_x, delta_y) order.
    candidate_shifts = np.column_stack((DX.ravel(), DY.ravel()))
    
    best_shift = None
    best_metric = np.inf
    
    # Compute current offset (in (x, y) order)
    current_offset = (current_center[0] - base_center[0], current_center[1] - base_center[1])
    
    for candidate in candidate_shifts:
        # Effective shift = current_offset + candidate, all in (x, y) order.
        effective_shift = (current_offset[0] + candidate[0], current_offset[1] + candidate[1])
        wedge_profiles, _ = compute_wedge_radial_profiles_shifted(
            image, mask, base_center, effective_shift, dx_base, dy_base,
            n_wedges=n_wedges, n_rad_bins=n_rad_bins)
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
        if metric < best_metric:
            best_metric = metric
            best_shift = candidate
        
    return best_shift  # Returns candidate shift as (dx, dy)

def find_diffraction_center(image, mask, threshold=0.01, max_iters=10, step_size=1.0, n_steps=3, 
                            n_wedges=8, n_rad_bins=200, verbose=False):
    # Precompute coordinate grids.
    rows, cols = np.indices(image.shape)
    
    base_center = center_of_mass_initial_guess(image, mask)
    
    # Compute differences relative to the base center.
    # Note: 'cols' are the x-coordinates, and 'rows' are the y-coordinates.
    dx_base = cols - base_center[0]  # x differences (columns)
    dy_base = rows - base_center[1]  # y differences (rows)
    
    center = base_center

    # Iterate to refine the center.
    for iteration in range(max_iters):
        candidate_shift = find_best_center_shift_vectorized(
            image, mask, center, base_center, dx_base, dy_base,
            step_size=step_size,
            n_steps=n_steps,
            n_wedges=n_wedges,
            n_rad_bins=n_rad_bins
        )
        dx, dy = candidate_shift  # extract shifts
        
        shift_mag = np.sqrt(dx**2 + dy**2)
        center = (center[0] + dx, center[1] + dy)
        
        if shift_mag < threshold:
            center = (float(center[0]), float(center[1]))
            if verbose:
                print(f"Converged after {iteration+1} iterations with center found at {center}")
            break
    
    return center 

def load_image_and_mask(image_file, mask_file, select_first=True):
    """
    Loads the diffraction image(s) and corresponding mask(one mask for all images) from HDF5 files.
    
    Args:
        image_file (str): Path to the HDF5 file containing '/entry/data/images'
        mask_file (str): Path to the HDF5 file containing '/mask'
        select_first (bool): If True, returns only the first image(and mask) pair.
                             If False, returns the full stack.
    
    Returns:
        image (np.ndarray): 2D array if select_first is True, or 3D array (stack) otherwise.
        mask (np.ndarray): 2D array if select_first is True, or 3D array (stack) otherwise.
    """
    with h5py.File(image_file, "r") as hf:
        image = hf["/entry/data/images"][:]
    with h5py.File(mask_file, "r") as hf:
        mask = hf["/mask"][:]
    
    if select_first:
        if image.ndim > 2:
            image = image[0]
        if mask.ndim > 2:
            mask = mask[0]
            
    return image.astype(np.float32), mask.astype(bool)
