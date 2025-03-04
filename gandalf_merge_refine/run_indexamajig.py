
import os
import subprocess

def run_indexamajig(x, y, geomfile_path, cellfile_path, input_path, output_folder, output_file_base, num_threads, extra_flags=None):

    if extra_flags is None:
        extra_flags = []

    output_file_name = f"{output_file_base}_{x}_{y}.stream"
    output_path = os.path.join(output_folder, output_file_name)
    listfile_path = os.path.join(input_path, 'list.lst')

    # Create a list of command parts
    command_parts = [
        "indexamajig",
        "-g", geomfile_path,
        "-i", listfile_path,
        "-o", output_path,
        "-p", cellfile_path,
        "-j", str(num_threads)
    ]

    # Append any extra flags provided by the user.
    command_parts.extend(extra_flags)

    # Join the parts into a single command string.
    base_command = " ".join(command_parts)
    subprocess.run(base_command, shell=True, check=True)
