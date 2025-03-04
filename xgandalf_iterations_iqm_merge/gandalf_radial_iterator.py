import os
import subprocess
from tqdm import tqdm

from list_h5_files import list_h5_files
from run_indexamajig import run_indexamajig
from gen_temp_geometry_file import gen_temp_geometry_file
from uniform_radial_xy_pairs import generate_sorted_grid_points

def gandalf_iterator(x, y, 
                     geomfile_path, 
                     cellfile_path, 
                     input_path, 
                     output_file_base, 
                     num_threads, 
                     max_radius=1, 
                     step=0.1, 
                     extra_flags=None
                     ):
    """
    Run CrystFEL's 'indexamajig' on a grid of beam centers.

    Args:
        x (float): Initial beam center X coordinate in pixels.
        y (float): Initial beam center Y coordinate in pixels.
        geomfile_path (str): Path to the .geom file.
        cellfile_path (str): Path to the .cell file containing cell parameters.
        input_path (str): Path to the folder where .h5 files reside (and where output is stored).
        output_file_base (str): Base name for output files (e.g., 'LTA'); final filenames will be 'base_x_y.h5'.
        num_threads (int): Number of CPU threads to use.
        max_radius (float): Maximum radius for the grid search, in pixels.
        step (float): Grid step size in pixels (the smaller, the finer the grid).
        extra_flags (list): Additional command-line flags to pass to 'indexamajig'.

    Returns:
        None. Outputs multiple .stream and .h5 files in the input_path folder.

    Notes:
        - The function performs a radial scan of beam centers around (x, y).
        - Each new (x, y) is processed with the same CrystFEL parameters.
        - Make sure CrystFEL is installed and in your PATH.
    """
    list_h5_files(input_path)
    output_folder = os.path.join(input_path, f"xgandalf_iterations_max_radius_{max_radius}_step_{step}")
    os.makedirs(output_folder, exist_ok   = True) 

    xdefault = -x
    ydefault = -y

    xy_pairs = list(generate_sorted_grid_points(xdefault, ydefault, max_radius=max_radius, step=step))
    
    # Iterate over all xy pairs
    for x, y in tqdm(xy_pairs, desc="Processing XY pairs"):
        print(f"Running for x={x}, y={y}")
        try:
            temp_geomfile_path = gen_temp_geometry_file(geomfile_path, x, y) 
            run_indexamajig(x, y, temp_geomfile_path, cellfile_path, input_path, output_folder, output_file_base, num_threads, extra_flags=extra_flags)

        except KeyboardInterrupt:
            print("Process interrupted by user.")
            break
        except subprocess.CalledProcessError as e:
            print(f"Error during indexamajig execution: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            if os.path.exists(temp_geomfile_path):
                os.remove(temp_geomfile_path)  # Ensure the file is deleted if not already done
