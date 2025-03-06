import numpy as np  
from utilities import center_of_mass_initial_guess
from compute_wedge_radial_profiles import compute_wedge_radial_profiles
import matplotlib.pyplot as plt
from find_best_center_shift import find_best_center_shift

def find_diffraction_center(image, mask, threshold=0.01, max_iters=10, step_size=1.0, n_steps=3, 
                            n_wedges=8, n_rad_bins=200, plot_profiles=False):
    """
    Iteratively refines the diffraction center.
    """
    center = center_of_mass_initial_guess(image, mask)
    print(f"Initial guess center: {center}")
    
    # Precompute indices once for the image shape.
    indices = np.indices(image.shape)  # returns a (2, height, width) array
    
    for iteration in range(max_iters):
        dx, dy = find_best_center_shift(
            image, mask, center,
            indices,  # pass precomputed
            step_size=step_size,
            n_steps=n_steps,
            n_wedges=n_wedges,
            n_rad_bins=n_rad_bins
        )
        shift_mag = np.sqrt(dx**2 + dy**2)
        center = (center[0] + dx, center[1] + dy)
        print(f"Iteration {iteration+1}: shift=({dx:.3f}, {dy:.3f}), "
              f"shift_mag={shift_mag:.3f}, new center={center}")
        
        if plot_profiles:
            wedge_profiles, radii = compute_wedge_radial_profiles(
                image, mask, center, indices,  # pass precomputed indices
                n_wedges=n_wedges, n_rad_bins=n_rad_bins
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
            print("Convergence reached.")
            break
    
    return center
