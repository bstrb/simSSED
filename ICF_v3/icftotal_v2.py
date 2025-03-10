# icftotal_v2.py

import h5py
import numpy as np
import numba
from multiprocessing import Pool, cpu_count

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


def _compute_shift_metric(args):
    """
    Helper function used for parallel metric evaluation.
    args is a tuple of:
       (shift, image, mask, base_center, dx_base, dy_base, n_wedges, n_rad_bins)
    We return (shift, metric).
    """
    (shift, image, mask, base_center, dx_base, dy_base, n_wedges, n_rad_bins) = args
    wedge_profiles, _ = compute_wedge_radial_profiles_shifted(
        image, mask, base_center, shift, dx_base, dy_base,
        n_wedges=n_wedges, n_rad_bins=n_rad_bins
    )
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
    return shift, metric

def find_best_center_shift_parallel(image, mask, current_center, base_center, dx_base, dy_base,
                                    step_size=1.0, n_steps=3, n_wedges=8, n_rad_bins=200):
    """
    Similar to find_best_center_shift_vectorized but uses multiprocessing Pool
    to evaluate all candidate shifts in parallel.
    Returns (dx, dy): the shift (relative to current_center) that gives the best metric.
    """
    # Create a grid of candidate shifts (in pixels).
    shift_vals = np.linspace(-step_size, step_size, n_steps)
    DX, DY = np.meshgrid(shift_vals, shift_vals)
    candidate_shifts_grid = np.column_stack((DX.ravel(), DY.ravel()))
    
    # Current offset in (x, y) order.
    # NOTE: The center is in (cx, cy) = (col, row) order in your code,
    # so we maintain consistency carefully. The base_center is also (cx, cy).
    current_offset = (current_center[0] - base_center[0],
                      current_center[1] - base_center[1])
    
    # Prepare the list of (shift, image, ...) arguments for parallel.
    args_list = []
    for candidate in candidate_shifts_grid:
        # The "effective center" is base_center + (current_offset + candidate).
        effective_shift = (current_offset[0] + candidate[0],
                           current_offset[1] + candidate[1])
        args_list.append((
            effective_shift, image, mask, base_center, dx_base, dy_base, n_wedges, n_rad_bins
        ))
    
    # Run everything in parallel
    # You can tweak processes=cpu_count() or a fixed number
    best_metric = np.inf
    best_shift = (0.0, 0.0)
    with Pool(processes=cpu_count()) as pool:
        for shift_val, metric in pool.map(_compute_shift_metric, args_list):
            if metric < best_metric:
                best_metric = metric
                # shift_val is the *effective* shift relative to base_center
                # We want to return the incremental shift relative to the
                # current_center. In other words,
                # shift_val = current_offset + candidate_shift
                # => candidate_shift = shift_val - current_offset
                best_shift = (shift_val[0] - current_offset[0],
                              shift_val[1] - current_offset[1])
    return best_shift


def find_diffraction_center(image, mask, threshold=0.01, max_iters=10,
                            step_size=1.0, n_steps=3, n_wedges=8, n_rad_bins=200,
                            use_parallel=True, verbose=False):
    """
    Main driver function that:
      1) Gets center of mass guess
      2) Iteratively refines by matching median wedge profiles across opposite wedges
         either in serial or in parallel (controlled by use_parallel).
    """
    rows, cols = np.indices(image.shape)
    
    base_center = center_of_mass_initial_guess(image, mask)
    
    # Precompute differences relative to the base center.
    # base_center is (cx, cy) = (col, row)
    dx_base = cols - base_center[0]  # x differences (columns)
    dy_base = rows - base_center[1]  # y differences (rows)
    
    center = base_center
    
    for iteration in range(max_iters):
        if use_parallel:
            candidate_shift = find_best_center_shift_parallel(
                image, mask, center, base_center, dx_base, dy_base,
                step_size=step_size, n_steps=n_steps,
                n_wedges=n_wedges, n_rad_bins=n_rad_bins
            )
        else:
            # If you still want the non-parallel version sometimes:
            candidate_shift = find_best_center_shift_vectorized(
                image, mask, center, base_center, dx_base, dy_base,
                step_size=step_size, n_steps=n_steps,
                n_wedges=n_wedges, n_rad_bins=n_rad_bins
            )
        
        dx, dy = candidate_shift
        shift_mag = np.sqrt(dx**2 + dy**2)
        center = (center[0] + dx, center[1] + dy)
        
        if shift_mag < threshold:
            center = (float(center[0]), float(center[1]))
            if verbose:
                print(f"Converged after {iteration+1} iterations with center found at {center}")
            break
    
    return center


def find_best_center_shift_vectorized(image, mask, current_center, base_center, dx_base, dy_base,
                                      step_size=1.0, n_steps=3, n_wedges=4, n_rad_bins=100):
    """
    Original serial version of scanning a grid of shifts to find minimal mismatch
    between opposite wedges. Provided here in case you want to switch between
    parallel and serial approaches.
    """
    # Create a grid of candidate shifts (in pixels).
    shift_vals = np.linspace(-step_size, step_size, n_steps)
    DX, DY = np.meshgrid(shift_vals, shift_vals)
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
            # The shift returned should be the incremental shift from current_center.
            best_shift = candidate
    
    return best_shift  # (dx, dy) relative to the current center.


def load_image_and_mask(image_file, mask_file, select_first=True):
    """
    Loads the diffraction image(s) and corresponding mask (one mask for all images) from HDF5 files.
    
    Args:
        image_file (str): Path to the HDF5 file containing '/entry/data/images'
        mask_file (str): Path to the HDF5 file containing '/mask'
        select_first (bool): If True, returns only the first image (and mask) pair.
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
