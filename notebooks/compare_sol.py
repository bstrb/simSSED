#!/usr/bin/env python3
"""
This script takes two .sol files as input. Each file is expected to have lines like:

    /Users/xiaodong/Desktop/simulations/UOX/simulation-43/sim.h5 //16 +0.0877521 +0.0730246 +0.0148768 -0.0877521 +0.0730246 +0.0148768 -0.0000000 -0.0231319 +0.0939282 0.000 0.000 oI

It will:
  - Skip the first token (the file path) and the last three tokens ("0.000 0.000 oI").
  - Use the identifier (the second token, e.g. "//16") as a key.
  - For each line that appears in both files (matched by the identifier), it divides the corresponding numeric entries from file1 (numerator) by file2 (denom).
  - If a denominator value is 0, it outputs “undefined” for that entry.
  - Finally, it prints a nicely formatted result.
  
Usage:
    python compare_sol.py file1.sol file2.sol
"""

import sys

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
    # if len(sys.argv) != 3:
    #     print("Usage: {} file1.sol file2.sol".format(sys.argv[0]))
    #     sys.exit(1)
    
    # file1_path = sys.argv[1]
    # file2_path = sys.argv[2]
    file2_path = "/Users/xiaodong/Desktop/simulations/UOX/simulation-43/orientation_matrices.sol"
    file1_path = "/Users/xiaodong/Desktop/simulations/UOX/simulation-43/UOXsim_-512.5_-512.5.sol"

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
        
        # Print the result for this identifier.
        print(f"Identifier {identifier}:")
        print("  Division results: " + " ".join(result))
        print()

if __name__ == "__main__":
    main()
