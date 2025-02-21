#!/usr/bin/env python3
import h5py
import os
import numpy as np

num_images = 523                     # Change the number of images as desired
output_dir = "/home/bubl3932/files/UOX_sim"
# Set the output file name and number of empty backgrounds to create
output_file = os.path.join(output_dir,f"{num_images}_empty_backgrounds.h5") # Change the file name/path as needed

def create_empty_backgrounds(output_file, num_images):
    # Define image dimensions and data type (matching the original images: 1024x1024, float32)
    image_shape = (1024, 1024)
    dtype = np.float32

    # The full dataset shape: (num_images, 1024, 1024)
    data_shape = (num_images,) + image_shape

    # Determine chunking:
    # If more than 1000 images are to be stored, use chunks of (1000, 1024, 1024).
    # Otherwise, use a single chunk for the entire dataset.
    if num_images > 1000:
        chunk_shape = (1000,) + image_shape
    else:
        chunk_shape = data_shape

    # Create the HDF5 file and dataset with the chosen chunking and fill value 0.
    with h5py.File(output_file, "w") as f:
        dset = f.create_dataset(
            "/entry/data/images",   # Dataset name
            shape=data_shape,
            dtype=dtype,
            chunks=chunk_shape,
            compression=None,  # No compression, matching your original dataset
            fillvalue=0        # All values set to 0 (i.e. "empty")
        )

        print(f"Created dataset 'backgrounds' in file: {output_file}")
        print("Dataset shape:    ", dset.shape)
        print("Data type:        ", dset.dtype)
        print("Chunk dimensions: ", dset.chunks)

if __name__ == "__main__":
    create_empty_backgrounds(output_file, num_images)
