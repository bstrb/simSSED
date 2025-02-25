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
  - Creates an interactive Plotly line plot for the division results.
  - The interactive plot includes an update menu so you can choose to display all values or a single chosen value.

Usage:
    python compare_sol.py file1.sol file2.sol
"""

import os
import sys
import csv
import numpy as np
import plotly.graph_objects as go

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

def compare_sol(file1_path, file2_path, plot=True):

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
    common_ids = list(set(data1.keys()) & set(data2.keys()))
    
    # Sort by the integer that follows "//". Example: "//16" -> 16
    def numeric_id(identifier):
        return int(identifier.replace("//", ""))  # assumes the part after // is always integer
    common_ids.sort(key=numeric_id)

    if not common_ids:
        print("No matching identifiers found in both files.")
        sys.exit(0)

    # We'll store the division results for CSV and plotting.
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
            # For example, we compute the absolute difference between the absolute values:
            res = abs(abs(a) - abs(b))
            result.append(f"{res:.5f}")

        division_results[identifier] = result

    # --- Write CSV output ---
    output_dir = os.path.dirname(file2_path)
    csv_output = os.path.join(output_dir, "compare_sol_abs_output.csv")
    # Determine the maximum number of numeric columns (they should be uniform for all common identifiers).
    max_cols = max(len(vals) for vals in division_results.values())

    with open(csv_output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Header: "identifier", then columns for each numeric result
        header = ["identifier"] + [f"value_{i}" for i in range(max_cols)]
        writer.writerow(header)

        for identifier in common_ids:
            row = [identifier] + division_results[identifier]
            writer.writerow(row)

    print(f"Division results have been written to '{csv_output}'.")

    # --- Create Interactive Plotly Plot ---
    if plot:
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

        # Convert to numpy array for easier slicing (rows: identifiers, columns: values)
        plot_data = np.array(plot_data, dtype=float)
        num_columns = plot_data.shape[1]

        # Create a Plotly figure with one trace per column.
        fig = go.Figure()
        for col in range(num_columns):
            fig.add_trace(go.Scatter(
                x=valid_identifiers,
                y=plot_data[:, col],
                mode='lines+markers',
                name=f"value_{col}"
            ))

        # Create update menu buttons:
        # The first button ("All") will display all traces.
        # Each subsequent button will display only one trace.
        buttons = [
            dict(label="All",
                 method="update",
                 args=[{"visible": [True]*num_columns},
                       {"title": "All values"}])
        ]
        for i in range(num_columns):
            visibility = [False] * num_columns
            visibility[i] = True
            buttons.append(dict(label=f"value_{i}",
                                method="update",
                                args=[{"visible": visibility},
                                      {"title": f"value_{i}"}]))

        fig.update_layout(
            updatemenus=[
                dict(
                    active=0,
                    buttons=buttons,
                    x=1.05,
                    y=1
                )
            ],
            title="Comparison of .sol Files",
            xaxis_title="Identifier",
            yaxis_title="Division Result (|file1| vs |file2|)",
            xaxis=dict(type='category')  # to keep the identifiers in order
        )

        # Save the interactive plot to an HTML file.
        html_output = os.path.join(output_dir, "plotly_comparison.html")
        fig.write_html(html_output)
        print(f"Interactive plot saved to '{html_output}'.")

# Example usage:
file1_path = "/home/bubl3932/files/UOX_sim/simulation-21/UOXsim_xgandalf_-512.5_-512.5.sol"
file2_path = "/home/bubl3932/files/UOX_sim/simulation-21/orientation_matrices.sol"
compare_sol(file1_path, file2_path, plot=True)
