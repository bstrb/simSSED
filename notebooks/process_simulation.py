import random
import h5py
from tqdm import tqdm
from typing import Any

def process_simulation(
    output_filename: str,
    simulations: Any,
    intensity_scale: float = 1000,
    calibration: float = 0.0015090274190359715,
    sigma: float = 1.5,
    fast_clip_threshold: float = 5
) -> None:
    """
    Opens the HDF5 file, generates simulated diffraction images, adds them to the existing dataset,
    and updates the Euler angles.

    Args:
        output_filename (str): Path to the output HDF5 file.
        simulations (Any): A simulations object that provides 'irot' and 'rotations'.
        intensity_scale (float): Scale factor for image intensity.
        calibration (float): Calibration constant.
        sigma (float): Sigma value for the diffraction pattern.
        fast_clip_threshold (float): Fast clip threshold parameter.
    """
    with h5py.File(output_filename, "r+") as data:
        images = data["entry"]["data"]["images"]
        euler_angles = data["entry"]["data"].require_dataset(
            "simulation_euler_angles", 
            shape=(images.shape[0], 3), 
            dtype=float
        )
        shape = images.shape[-2:]
        for i in tqdm(range(images.shape[0]), desc="Processing images"):
            in_plane = random.uniform(0, 360)
            ind = random.randint(0, simulations.current_size - 1)
            img = simulations.irot[ind].get_diffraction_pattern(
                shape=shape,
                direct_beam_position=(shape[0] // 2, shape[1] // 2),
                sigma=sigma,
                in_plane_angle=in_plane,
                calibration=calibration,
                fast=False,
                normalize=True,
                fast_clip_threshold=fast_clip_threshold
            )
            img = (img * intensity_scale).astype(images.dtype)
            images[i] += img
            euler_angles_i = simulations.rotations[ind].to_euler(degrees=True).squeeze()
            euler_angles_i[0] = in_plane  # Override first Euler angle.
            euler_angles[i] = euler_angles_i
    print("Processing complete. Updated file saved at:", output_filename)
