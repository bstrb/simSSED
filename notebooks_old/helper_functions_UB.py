import os
import shutil
import h5py
import matplotlib.pyplot as plt
from IPython.display import clear_output
from typing import Tuple, Any, Optional
import numpy as np

# def get_next_simulation_folder(base_dir: str, prefix: str = "simulation") -> str:
#     folder_number = 1
#     while os.path.exists(os.path.join(base_dir, f"{prefix}-{folder_number}")):
#         folder_number += 1
#     new_folder = os.path.join(base_dir, f"{prefix}-{folder_number}")
#     os.makedirs(new_folder)
#     return new_folder
from pathlib import Path

def get_next_simulation_folder(base_dir: Path) -> Path:
    """
    Create a sub-folder named sim_000, sim_001, … and return it as a Path.
    """
    base_dir = Path(base_dir)
    existing = sorted(base_dir.glob("sim_*"))
    next_idx = len(existing)
    new_folder = base_dir / f"sim_{next_idx:03d}"
    new_folder.mkdir(parents=True, exist_ok=True)
    return new_folder

def copy_h5_file(src: str, dst: str) -> None:
    shutil.copyfile(src, dst)

def load_h5_data(filename: str) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Loads images and, if present, simulation Euler angles from an HDF5 file.

    Returns:
        (images_arr, orientation_matrices):
            - images_arr: the Numpy array of images
            - orientation_matrices: the orientation matrices, or None if not found
    """
    with h5py.File(filename, "r") as hf:
        images_arr = hf["entry"]["data"]["images"][:]
        data_group = hf["entry"]["data"]
        if "simulation_orientation_matrices" in data_group:
            orientation_matrices = data_group["simulation_orientation_matrices"][:]
        else:
            orientation_matrices = None
    return images_arr, orientation_matrices

def view_image(index: int, images_arr, orientation_matrices) -> None:
    """
    Displays the image and its Orientation matrix for the given index, if matrix available.
    """
    clear_output(wait=True)
    img = images_arr[index]
    if orientation_matrices is not None:
        matrices = orientation_matrices[index]
        matrices_str = f"Orientation matrix: {matrices}"
    else:
        matrices_str = "No Orientation matrices"
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap="gray")
    plt.title(f"Image Index: {index}\n{matrices_str}")
    plt.axis("off")
    plt.show()

