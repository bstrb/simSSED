#!/usr/bin/env python3
import os
import h5py
import numpy as np
import pandas as pd

def create_updated_h5(original_h5_path, new_h5_path, csv_path, framesize=1024, pixels_per_meter=17857.14285714286):
    """
    Create a new HDF5 file by copying the original file's structure,
    update the center_x and center_y datasets using CSV data, and
    recalculate detector shifts (det_shift_x_mm and det_shift_y_mm).

    Parameters
    ----------
    original_h5_path : str
        Path to the original HDF5 file.
    new_h5_path : str
        Path where the updated HDF5 file will be created.
    csv_path : str
        Path to the CSV file containing updated centers (columns: center_x, center_y).
    framesize : int, optional
        Size of the frame (assumed square) used for recalculating shifts (default is 1024).
    pixels_per_meter : float, optional
        Conversion factor from pixels to meters (default is 17857.14285714286).
    """
    # 1. Read updated centers from the CSV file
    df = pd.read_csv(csv_path)
    if not all(col in df.columns for col in ['center_x', 'center_y']):
        raise ValueError("CSV file must contain 'center_x' and 'center_y' columns")
    center_x = df['center_x'].values
    center_y = df['center_y'].values

    # 2. Copy the original HDF5 file structure into a new file
    with h5py.File(original_h5_path, 'r') as src, h5py.File(new_h5_path, 'w') as dst:
        src.copy('entry', dst)

    # 3. Reopen the new file in read-write mode to update datasets
    with h5py.File(new_h5_path, 'r+') as dst:
        # Remove existing center_x and center_y datasets if they exist
        if 'entry/data/center_x' in dst:
            del dst['entry/data/center_x']
        if 'entry/data/center_y' in dst:
            del dst['entry/data/center_y']
        dst.create_dataset('entry/data/center_x', data=center_x, dtype='float64')
        dst.create_dataset('entry/data/center_y', data=center_y, dtype='float64')

        # 4. Compute the new detector shifts
        presumed_center = framesize / 2.0
        det_shift_x_mm = -((center_x - presumed_center) / pixels_per_meter) * 1000
        det_shift_y_mm = -((center_y - presumed_center) / pixels_per_meter) * 1000

        # Remove existing detector shift datasets if they exist
        if 'entry/data/det_shift_x_mm' in dst:
            del dst['entry/data/det_shift_x_mm']
        if 'entry/data/det_shift_y_mm' in dst:
            del dst['entry/data/det_shift_y_mm']
        dst.create_dataset('entry/data/det_shift_x_mm', data=det_shift_x_mm, dtype='float64')
        dst.create_dataset('entry/data/det_shift_y_mm', data=det_shift_y_mm, dtype='float64')

    print(f"New HDF5 file created: {new_h5_path}")
    print("Center coordinates and detector shifts have been updated.")


if __name__ == '__main__':
    # Modify these paths as needed
    original_h5_path = "/home/bubl3932/files/UOX1/UOX1_original/UOX1_sub/UOX1_subset.h5"
    new_h5_path = "/home/bubl3932/files/UOX1/UOX1_original/UOX1_sub/UOX1_subset_UPDATED.h5"
    csv_path = "/home/bubl3932/files/UOX1/UOX1_original/UOX1_sub/filtered_centers.csv"
    
    create_updated_h5(original_h5_path, new_h5_path, csv_path)
