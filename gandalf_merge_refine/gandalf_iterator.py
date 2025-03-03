import os
import subprocess
from tqdm import tqdm

from list_h5_files import list_h5_files
from gen_temp_geometry_file import gen_temp_geometry_file
from run_indexamajig import run_indexamajig
# from generate_xy_pairs import generate_xy_pairs
from generate_random_xy_pairs_within_radius import generate_xy_pairs
 
def gandalf_iterator(x, y, 
                     geomfile_path, 
                     cellfile_path, 
                     input_path, 
                     output_file_base, 
                     num_threads, 
                     step=0.01, 
                     layers=1, 
                     extra_flags=None
                     ):
    
    list_h5_files(input_path)

    xdefault = -x
    ydefault = -y

    # Generate xy pairs including the default coordinates
    # xy_pairs = [(xdefault, ydefault)] + list(generate_xy_pairs(xdefault, ydefault, radius=1, num_points=20, decimals=1))
    xy_pairs = list(generate_xy_pairs(xdefault, ydefault, radius=1, num_points=20, decimals=1))

    # Iterate over all xy pairs
    for x, y in tqdm(xy_pairs, desc="Processing XY pairs"):
        print(f"Running for x={x}, y={y}")
        try:
            temp_geomfile_path = gen_temp_geometry_file(geomfile_path, x, y) 
            run_indexamajig(x, y, temp_geomfile_path, cellfile_path, input_path, output_file_base, num_threads, extra_flags=extra_flags)

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
