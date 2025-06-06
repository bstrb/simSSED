import os
import subprocess
import time
from tqdm import tqdm

from convert_hkl_to_mtz import convert_hkl_to_mtz

def run_partialator(stream_file, output_dir, num_threads, pointgroup, iterations):
    """
    Run the 'partialator' command to process a single stream file.
    Monitors progress by reading 'Residuals:' lines in stderr.
    """
    merging_cmd = [
        'partialator',
        stream_file,
        '--model=offset',
        '-j', f'{num_threads}',
        '-o', os.path.join(output_dir, "crystfel.hkl"),
        '-y', pointgroup,
        '--polarisation=none',
        '--min-measurements=2',
        '--max-adu=inf',
        '--min-res=inf',
        '--push-res=inf',
        '--no-Bscale',
        '--no-logs',
        f'--iterations={iterations}',
        '--harvest-file=' + os.path.join(output_dir, "parameters.json"),
        '--log-folder=' + os.path.join(output_dir, "pr-logs")
    ]

    stderr_path = os.path.join(output_dir, "stderr.log")
    total_residuals = iterations + 2  # Heuristic for how many 'Residuals:' lines show up

    try:
        with open(os.path.join(output_dir, "stdout.log"), "w") as stdout, \
             open(stderr_path, "w") as stderr:
            
            print(f"Running partialator for stream file: {stream_file}")
            progress = tqdm(total=total_residuals, desc="Partialator Progress", unit="Residual")
            
            # Launch partialator
            process = subprocess.Popen(merging_cmd, stdout=stdout, stderr=stderr)

            # Monitor progress by checking the stderr file for "Residuals:" lines
            while process.poll() is None:
                time.sleep(1)
                if os.path.exists(stderr_path):
                    with open(stderr_path, "r") as f:
                        residual_count = sum(1 for line in f if line.startswith("Residuals:"))
                        progress.n = min(residual_count, total_residuals)
                        progress.refresh()

            process.communicate()  # Ensure process has fully completed
            progress.n = total_residuals
            progress.refresh()
            progress.close()

            print(f"Partialator completed for stream file: {stream_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error during partialator execution for {stream_file}: {e}")
        raise
    finally:
        # Ensure we close the progress bar even if there's an exception
        progress.close()

def run_partialator_and_convert(
    stream_file: str,
    pointgroup: str="P1",
    num_threads: int=1,
    iterations: int=3,
    convert_to_mtz=False,
    cell_file: str=None  # optional; not needed if convert_to_mtz is False
):
    """
    High-level function to run partialator on a single stream file and then optionally convert to MTZ(if cell file is provided as a string).
    Creates an output folder based on the stream_file name and iteration number.
    Returns the path to the output directory for further inspection if needed.
    
    Input Parameters:

    stream_file: The input file to process. Although now optional if MTZ conversion is not needed.
    
    pointgroup: Specifies the crystallographic point group; default is "P1".

    num_threads: Number of threads to use, allowing parallel processing (default is 1).

    iterations: Determines how many iterations the partialator will run (default is 3).

    convert_to_mtz: A flag that, if set to True, will trigger an additional conversion step from HKL format to MTZ format.

    cell_file: A required file for conversion when convert_to_mtz is True; otherwise, it is not needed.

    """
    output_dir = os.path.splitext(stream_file)[0] + f"_merge_{iterations}_iter"

    # Create the output directory and the pr-logs subdirectory
    os.makedirs(os.path.join(output_dir, "pr-logs"), exist_ok=True)

    # Run partialator
    try:
        run_partialator(stream_file, output_dir, num_threads, pointgroup, iterations)
    except subprocess.CalledProcessError:
        print(f"Failed partialator run for {stream_file}. Aborting conversion.")
        return None
    
    if convert_to_mtz:
        if cell_file is None:
            raise ValueError("A cell file must be provided when convert_to_mtz is True.")
        try:
            convert_hkl_to_mtz(output_dir, cell_file)
            print(f"Conversion to MTZ successful. Output in: {output_dir}")
        except Exception as e:
            print(f"Failed to convert HKL to MTZ: {e}")
            return None

    return output_dir
