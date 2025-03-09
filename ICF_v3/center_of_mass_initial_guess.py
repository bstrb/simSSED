import numpy as np

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