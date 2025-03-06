import h5py
import numpy as np

def load_image_and_mask(image_file, mask_file, select_first=True):
    """
    Loads the diffraction image(s) and corresponding mask from HDF5 files.
    
    Args:
        image_file (str): Path to the HDF5 file containing '/entry/data/images'
        mask_file (str): Path to the HDF5 file containing '/mask'
        select_first (bool): If True, returns only the first image/mask pair.
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
