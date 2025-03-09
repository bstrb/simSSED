# process_image.py

from find_diffraction_center import find_diffraction_center

def process_image(frame_number, image, masks, threshold, max_iters, step_size, n_steps, n_wedges, n_rad_bins):
    """
    Process a single image frame to find its diffraction center.
    
    Parameters:
        frame_number (int): The frame number (or index).
        image (np.ndarray): The image data.
        masks (np.ndarray): The mask array.
        threshold (float): Convergence threshold.
        max_iters (int): Maximum number of iterations.
        step_size (float): Step size for the grid search.
        n_steps (int): Number of steps in each direction for grid search.
        n_wedges (int): Number of angular wedges.
        n_rad_bins (int): Number of radial bins.
        
    Returns:
        tuple: (frame_number, center) where center is the computed diffraction center.
    """
    center = find_diffraction_center(
        image,
        masks,
        threshold=threshold,
        max_iters=max_iters,
        step_size=step_size,
        n_steps=n_steps,
        n_wedges=n_wedges,
        n_rad_bins=n_rad_bins,
        verbose=True
    )
    return frame_number, center
