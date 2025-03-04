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
