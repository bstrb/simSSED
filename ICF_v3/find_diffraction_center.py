import numpy as np  
from center_of_mass_initial_guess import center_of_mass_initial_guess
from find_best_center_shift_vectorized import find_best_center_shift_vectorized

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
