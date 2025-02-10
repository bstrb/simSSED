import random

from .data import get_raw_data
from .simulation import get_simulations, get_simulations_from_cif

def main():
    
    # data = get_raw_data()
    # images = data["entry"]["data"]["images"]
    # sim_images = data["entry"]["data"].require_dataset("simulations", shape=images.shape, dtype=images.dtype)
    # euler_angles = data["entry"]["data"].require_dataset("euler_angles", shape=(images.shape[0], 3), dtype=float)
    # sims = get_simulations_from_cif()
    sims = get_simulations()
    sims.plot(interactive=True, show_labels=True, min_label_intensity=1.5)
    from matplotlib import pyplot as plt
    # plt.show()
    return
    shape = images.shape[-2:]
    calibration = 1 / 3.9 / 183
    intensity_scale = 1000 # max intensity of diffraction patterns
    from tqdm import tqdm
    for i in tqdm(range(images.shape[0])):
        in_plane = random.uniform(0, 360)
        ind = random.randint(0, sims.current_size - 1)
        img = sims.irot[ind].get_diffraction_pattern(
            shape=shape,
            sigma=1,
            in_plane_angle=in_plane,
            calibration=calibration,
        )
        img = (img * intensity_scale).astype(images.dtype)
        images[i] += img
        euler_angles_i = sims.rotations[ind].to_euler(degrees=True).squeeze()
        euler_angles_i[0] = in_plane
        euler_angles[i] = euler_angles_i
        sim_images[i] = img
    
if __name__ == "__main__":
    main()
