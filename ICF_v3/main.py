# main.py
import os
import h5py
import numpy as np
import pandas as pd
import time
from multiprocessing import Pool

from image_processing import process_single_image

def load_chunk(image_file, start, end):
    """
    Load a chunk of images from the H5 file.
    Slicing the dataset loads only the required subset.
    """
    with h5py.File(image_file, 'r') as f:
        images = f['/entry/data/images']
        # Slicing loads only the required images.
        chunk = images[start:end].astype(np.float32)
    return chunk

def process_images(image_file, mask_file, n_wedges, n_rad_bins, xatol, fatol, chunk_size, verbose):
    # Load the mask (once).
    with h5py.File(mask_file, 'r') as f_mask:
        mask = f_mask['/mask'][:].astype(bool)

    # Open the image file to determine the total number of images.
    with h5py.File(image_file, 'r') as f_img:
        n_images = f_img['/entry/data/images'].shape[0]

    # Define output CSV file path.
    csv_file = os.path.join(os.path.dirname(image_file), f"centers_xatol_{xatol}_fatol_{fatol}.csv")
    if os.path.exists(csv_file):
        os.remove(csv_file)
    header_written = False
    frame_counter = 0
    start_time = time.time()

    # Create a multiprocessing Pool.
    with Pool() as pool:
        for start_idx in range(0, n_images, chunk_size):
            end_idx = min(start_idx + chunk_size, n_images)
            current_chunk = load_chunk(image_file, start_idx, end_idx)
            
            # Prepare arguments for each image.
            args = [(img, mask, n_wedges, n_rad_bins, xatol, fatol, verbose) for img in current_chunk]
            
            # Process images in parallel.
            results = pool.starmap(process_single_image, args)
            
            # Write results incrementally.
            df_chunk = pd.DataFrame(
                [[frame_counter + idx, res[0], res[1]] for idx, res in enumerate(results)],
                columns=["frame_number", "center_x", "center_y"]
            )
            mode = "w" if not header_written else "a"
            df_chunk.to_csv(csv_file, index=False, mode=mode, header=not header_written)
            header_written = True
            frame_counter += len(results)
            print(f"Processed frames {start_idx} to {end_idx}")
            
    elapsed = time.time() - start_time
    print("Processing complete in {:.1f}s".format(elapsed))
    print("CSV file written to:", csv_file)

if __name__ == '__main__':
    # Parameters – adjust these as needed.
    image_file = "/Users/xiaodong/Desktop/UOX-data/UOX1_sub/UOX1_sub.h5"
    mask_file = "/Users/xiaodong/mask/pxmask.h5"
    n_wedges = 4
    n_rad_bins = 100
    xatol = 0.01
    fatol = 10
    chunk_size = 100
    verbose = True

    process_images(image_file, mask_file, n_wedges, n_rad_bins, xatol, fatol, chunk_size, verbose)
