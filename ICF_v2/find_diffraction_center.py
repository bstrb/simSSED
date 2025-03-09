# find_diffraction_center.py
import numpy as np  
import matplotlib.pyplot as plt

from center_of_mass_initial_guess import center_of_mass_initial_guess
from compute_wedge_radial_profiles_shifted import compute_wedge_radial_profiles_shifted
from find_best_center_shift_vectorized import find_best_center_shift_vectorized

def find_diffraction_center(image, mask, threshold=0.01, max_iters=10, step_size=1.0, n_steps=3, 
                            n_wedges=8, n_rad_bins=200, plot_profiles=False, desired_threshold=None, verbose=False):
    # Precompute coordinate grids.
    rows, cols = np.indices(image.shape)
    base_center = center_of_mass_initial_guess(image, mask)
    
    # Precompute differences relative to base_center.
    dy_base = rows - base_center[0]
    dx_base = cols - base_center[1]
    
    # Start at the base center.
    center = base_center

    # Iterate over a fixed number of iterations (no inner progress bar)
    for iteration in range(max_iters):
        candidate_shift = find_best_center_shift_vectorized(
            image, mask, center, base_center, dx_base, dy_base,
            step_size=step_size,
            n_steps=n_steps,
            n_wedges=n_wedges,
            n_rad_bins=n_rad_bins
        )
        dy, dx = candidate_shift  # candidate shift (delta_y, delta_x)
        shift_mag = np.sqrt(dy**2 + dx**2)
        center = (center[0] + dy, center[1] + dx)
        
        if plot_profiles:
            effective_shift = (center[0] - base_center[0], center[1] - base_center[1])
            wedge_profiles, radii = compute_wedge_radial_profiles_shifted(
                image, mask, base_center, effective_shift, dx_base, dy_base,
                n_wedges=n_wedges, n_rad_bins=n_rad_bins,
                max_intensity=desired_threshold  # <-- your chosen intensity threshold
            )
            plt.figure()
            for w, prof in enumerate(wedge_profiles):
                plt.plot(radii, prof, label=f"Wedge {w}")
            plt.title(f"Iteration {iteration+1} Wedge Profiles")
            plt.xlabel("Radius (pixels)")
            plt.ylabel("Median Intensity")
            plt.legend()
            plt.show()
        
        if shift_mag < threshold:
            center = (float(center[0]), float(center[1]))
            if verbose and center is not None:
                print(f"Converged after {iteration+1} iterations with center found at {center}")
            break
    
    return center
