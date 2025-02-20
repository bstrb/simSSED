#!/usr/bin/env python3
"""
This script takes two .sol files as input. Each file is expected to have lines like:

    /path/to/sim.h5 //16 +0.0877521 +0.0730246 +0.0148768 -0.0877521 +0.0730246 +0.0148768 -0.0000000 -0.0231319 +0.0939282 0.000 0.000 oI

It will:
  - Skip the first token (the file path) and the last three tokens ("0.000 0.000 oI").
  - Use the identifier (the second token, e.g. "//16") as a key.
  - For each line that appears in both files (matched by the identifier), it divides the corresponding numeric entries from file1 (numerator) by file2 (denominator).
  - If a denominator value is 0, it outputs "undefined" for that entry.
  - Writes all division results into a CSV file.
  - Creates a simple line plot for the division results.

Usage:
    python compare_sol.py file1.sol file2.sol
"""

import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

def parse_line(line):
    """
    Parses a line from the .sol file.

    Expected line format:
      <filepath> <identifier> <num1> <num2> ... <numN> <tokenX> <tokenY> <tokenZ>

    It skips the file path (first token) and the last three tokens.
    Returns the identifier (e.g. "//16") and a list of floats.
    """
    tokens = line.strip().split()
    # Expect at least a file path, an identifier, some numbers, and three tokens at the end.
    if len(tokens) < 5:
        return None, []
    # Skip the first token (file path)
    identifier = tokens[1]  # e.g., "//16"
    # The remaining numeric tokens are from token index 2 to token index -3 (exclusive)
    num_tokens = tokens[2:-3]
    try:
        numbers = [float(tok) for tok in num_tokens]
    except ValueError:
        numbers = []
    return identifier, numbers

def main():
    
    file1_path = "/Users/xiaodong/Desktop/simulations/UOX/simulation-43/UOXsim_-512.5_-512.5.sol"
    file2_path = "/Users/xiaodong/Desktop/simulations/UOX/simulation-43/orientation_matrices.sol"

    # Dictionaries to hold data, keyed by identifier.
    data1 = {}
    data2 = {}

    # Read file1.
    with open(file1_path, 'r') as f1:
        for line in f1:
            if not line.strip():
                continue  # skip empty lines
            identifier, numbers = parse_line(line)
            if identifier:
                data1[identifier] = numbers

    # Read file2.
    with open(file2_path, 'r') as f2:
        for line in f2:
            if not line.strip():
                continue
            identifier, numbers = parse_line(line)
            if identifier:
                data2[identifier] = numbers

    # Find common identifiers between both files.
    common_ids = sorted(set(data1.keys()) & set(data2.keys()))
    if not common_ids:
        print("No matching identifiers found in both files.")
        sys.exit(0)

    # We'll store the division results for plotting and CSV.
    division_results = {}  # key = identifier, value = list of (float or "undefined")

    # Process each common line.
    for identifier in common_ids:
        nums1 = data1[identifier]
        nums2 = data2[identifier]
        if len(nums1) != len(nums2):
            print(f"Warning: Identifier {identifier} has mismatched number of entries between files.")
            continue

        result = []
        for a, b in zip(nums1, nums2):
            # If the denominator is 0 (or very close), mark as undefined.
            if abs(b) < 1e-12:
                result.append("undefined")
            else:
                result.append(f"{a / b:.5f}")

        division_results[identifier] = result

    # --- Write CSV output ---
    dir = os.path.dirname(file1_path)
    csv_output = os.path.join(dir, "compare_sol_output.csv")
    # Determine the maximum number of numeric columns (they should be uniform for all common identifiers).
    max_cols = 0
    for identifier in division_results:
        max_cols = max(max_cols, len(division_results[identifier]))

    with open(csv_output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Header: "identifier", then columns for each numeric result
        header = ["identifier"] + [f"value_{i}" for i in range(max_cols)]
        writer.writerow(header)

        for identifier in common_ids:
            row = [identifier] + division_results[identifier]
            writer.writerow(row)

    print(f"Division results have been written to '{csv_output}'.")

    # --- Plot the results ---
    # Convert the "undefined" strings to np.nan for plotting.
    # We'll create a 2D array, rows = identifiers, columns = each numeric value
    plot_data = []
    valid_identifiers = []
    for identifier in common_ids:
        row_values = []
        has_valid = False
        for val in division_results[identifier]:
            if val == "undefined":
                row_values.append(np.nan)
            else:
                row_values.append(float(val))
                has_valid = True
        if has_valid:  # only keep rows that have at least one numeric value
            plot_data.append(row_values)
            valid_identifiers.append(identifier)

    if not plot_data:
        print("No valid numeric data to plot.")
        sys.exit(0)

    # Convert to numpy array for easier slicing: shape = (num_identifiers, num_columns)
    plot_data = np.array(plot_data, dtype=float)
    x = np.arange(len(valid_identifiers))  # x positions for each identifier

    plt.figure(figsize=(10, 6))
    # Plot one line per column
    num_columns = plot_data.shape[1]
    for col in range(num_columns):
        y = plot_data[:, col]
        plt.plot(x, y, marker='o', label=f"value_{col}")

    plt.xticks(x, valid_identifiers, rotation=90)
    plt.xlabel("Identifier")
    plt.ylabel("Division Result (file1 / file2)")
    plt.title("Comparison of .sol Files")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
