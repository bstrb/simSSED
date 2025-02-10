import os
import shutil
import h5py
import matplotlib.pyplot as plt
from IPython.display import clear_output
from typing import Tuple, Any

def get_next_simulation_folder(base_dir: str, prefix: str = "simulation") -> str:
    """
    Finds the next available simulation folder with the given prefix and creates it.

    Args:
        base_dir (str): The base directory to search in.
        prefix (str): The folder prefix (default "simulation").

    Returns:
        str: The full path to the newly created simulation folder.
    """
    folder_number = 1
    while os.path.exists(os.path.join(base_dir, f"{prefix}-{folder_number}")):
        folder_number += 1
    new_folder = os.path.join(base_dir, f"{prefix}-{folder_number}")
    os.makedirs(new_folder)
    return new_folder

def copy_h5_file(src: str, dst: str) -> None:
    """
    Copies an HDF5 file from src to dst.

    Args:
        src (str): Source file path.
        dst (str): Destination file path.
    """
    shutil.copyfile(src, dst)

def load_h5_data(filename: str) -> Tuple[Any, Any]:
    """
    Loads images and simulation Euler angles from an HDF5 file.

    Args:
        filename (str): Path to the HDF5 file.

    Returns:
        Tuple: A tuple containing the images array and Euler angles array.
    """
    with h5py.File(filename, "r") as hf:
        images_arr = hf["entry"]["data"]["images"][:]
        angles_arr = hf["entry"]["data"]["simulation_euler_angles"][:]
    return images_arr, angles_arr

def view_image(index: int, images_arr, angles_arr) -> None:
    """
    Clears the current output and displays the image and its Euler angles for the given index.

    Args:
        index (int): Index of the image.
        images_arr: Numpy array of images.
        angles_arr: Numpy array of Euler angles.
    """
    clear_output(wait=True)
    img = images_arr[index]
    angles = angles_arr[index]
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap="gray")
    plt.title(f"Image Index: {index}\nEuler Angles: {angles}")
    plt.axis("off")
    plt.show()
