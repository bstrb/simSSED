import os
import h5py
import numpy as np
from tqdm import tqdm

def compute_radial_background_centered(image, obj_cx, obj_cy):
    """
    Compute a radial mean background from an image using the provided object center,
    and then re-map (spread) that radial profile so that the background is centered at
    the geometric center of the image.
    
    Parameters:
      image : 2D numpy array
          The input image.
      obj_cx, obj_cy : float
          The x and y coordinates of the object (from the file), which may be off-center.
    
    Returns:
      background : 2D numpy array
          The computed radial background image, recentered so that its symmetry is about the image center.
    """
    # --- Step 1: Compute the radial mean profile using the provided object center ---
    # Create coordinate grids for the input image.
    y_indices, x_indices = np.indices(image.shape)
    # Compute distance from each pixel to the object’s center.
    r_obj = np.sqrt((x_indices - obj_cx)**2 + (y_indices - obj_cy)**2)
    # Map each pixel to an integer radius (1-pixel bins)
    r_obj_int = np.floor(r_obj).astype(np.int64)
    
    # Compute the sum and count of pixel values for each radius using np.bincount.
    max_bin = r_obj_int.max() + 1
    sum_vals = np.bincount(r_obj_int.ravel(), weights=image.ravel(), minlength=max_bin)
    count_vals = np.bincount(r_obj_int.ravel(), minlength=max_bin)
    # Calculate the radial mean profile (avoid division by zero)
    radial_means = sum_vals / np.maximum(count_vals, 1)
    
    # --- Step 2: Re-map the radial profile to a new image centered at the image center ---
    # Define the geometric center of the image.
    center_x = image.shape[1] / 2
    center_y = image.shape[0] / 2
    # Create coordinate grids for the output image.
    y_out, x_out = np.indices(image.shape)
    # Compute distance from each pixel to the geometric center.
    r_center = np.sqrt((x_out - center_x)**2 + (y_out - center_y)**2)
    # Convert these distances to integer bins.
    r_center_int = np.floor(r_center).astype(np.int64)
    # Clip the radii so that we do not exceed the length of our radial profile.
    r_center_int = np.clip(r_center_int, 0, len(radial_means) - 1)
    
    # Build the output background image by mapping each pixel's distance (from the image center)
    # to the corresponding radial mean.
    background = radial_means[r_center_int]
    
    # Return the background cast to the same type as the original image.
    return background.astype(image.dtype)

def main():
    # Input and output file paths.
    input_file = "/Users/xiaodong/Desktop/UOXs-2/UOXs.h5"
    output_file = os.path.join(os.path.dirname(input_file), "UOXs_radial_backgrounds.h5")
    
    # Open the input file.
    with h5py.File(input_file, "r") as f:
        # Load the images and center positions.
        images = f["/entry/data/images"]
        center_x_arr = f["/entry/data/center_x"][:]  # Expect shape (n_images,)
        center_y_arr = f["/entry/data/center_y"][:]  # Expect shape (n_images,)
        
        n_images = images.shape[0]
        image_shape = images.shape[1:]  # e.g., (height, width)
        dtype = images.dtype
        
        # Preallocate an array for the computed radial background images.
        backgrounds = np.empty((n_images, *image_shape), dtype=dtype)
        
        # Process each image.
        for i in tqdm(range(n_images), desc="Computing radial backgrounds"):
            img = images[i]
            # Get the object center (which may be off-center).
            obj_cx = center_x_arr[i]
            obj_cy = center_y_arr[i]
            # Compute the radial background and re-center it.
            backgrounds[i] = compute_radial_background_centered(img, obj_cx, obj_cy)
    
    # Write the computed backgrounds to a new HDF5 file.
    # The dataset is placed at /entry/data/images, exactly as in the original file.
    with h5py.File(output_file, "w") as f_out:
        grp_entry = f_out.require_group("entry")
        grp_data = grp_entry.require_group("data")
        grp_data.create_dataset("images", data=backgrounds, dtype=dtype)
    
    print("Done! Radial background images saved to:", output_file)

if __name__ == "__main__":
    main()
