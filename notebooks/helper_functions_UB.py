import os
import shutil
import h5py
import matplotlib.pyplot as plt
from IPython.display import clear_output
from typing import Tuple, Any, Optional
import numpy as np

def get_next_simulation_folder(base_dir: str, prefix: str = "simulation") -> str:
    folder_number = 1
    while os.path.exists(os.path.join(base_dir, f"{prefix}-{folder_number}")):
        folder_number += 1
    new_folder = os.path.join(base_dir, f"{prefix}-{folder_number}")
    os.makedirs(new_folder)
    return new_folder

def copy_h5_file(src: str, dst: str) -> None:
    shutil.copyfile(src, dst)

def load_h5_data(filename: str) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Loads images and, if present, simulation Euler angles from an HDF5 file.

    Returns:
        (images_arr, angles_arr):
            - images_arr: the Numpy array of images
            - angles_arr: the Numpy array of Euler angles, or None if not found
    """
    with h5py.File(filename, "r") as hf:
        images_arr = hf["entry"]["data"]["images"][:]
        data_group = hf["entry"]["data"]
        if "simulation_orientation_matrices" in data_group:
            angles_arr = data_group["simulation_orientation_matrices"][:]
        else:
            angles_arr = None
    return images_arr, angles_arr

def view_image(index: int, images_arr, angles_arr) -> None:
    """
    Displays the image and its Orientation matrix for the given index, if matrix available.
    """
    clear_output(wait=True)
    img = images_arr[index]
    if angles_arr is not None:
        angles = angles_arr[index]
        angle_str = f"Orientation matrix: {angles}"
    else:
        angle_str = "No Orientation matrices"
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap="gray")
    plt.title(f"Image Index: {index}\n{angle_str}")
    plt.axis("off")
    plt.show()

