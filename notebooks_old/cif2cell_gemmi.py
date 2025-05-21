#!/usr/bin/env python3
"""
cif2cell_gemmi.py

Read a CIF file and write a CrystFEL .cell file (version 1.0) or output a 2-letter Bravais code using Gemmi.

Usage:
    # Write .cell file and show Bravais code:
    python3 cif2cell_gemmi.py input.cif -o output.cell

    # Only print the 2-letter Bravais lattice code (e.g. aP, tI):
    python3 cif2cell_gemmi.py input.cif --code

    # Default: write .cell in same folder as input with .cell extension
    python3 cif2cell_gemmi.py input.cif

Requires:
    pip install gemmi
"""
import os
import re
import argparse
import gemmi

# Conventional unique axis mapping by crystal system
UNIQUE_AXIS = {
    'triclinic':     None,
    'monoclinic':    'b',
    'orthorhombic':  None,
    'tetragonal':    'c',
    'rhombohedral':  'c',
    'hexagonal':     'c',
    'cubic':         None
}

# define your hard-coded defaults here:
AXIS_MAP = {
'monoclinic':    'b',
'tetragonal':    'c',
'hexagonal':     'c',
'trigonal':      'c',
'rhombohedral':  'c',
# orthorhombic, cubic, triclinic → no unique_axis entry
}

# First-letter mapping for Bravais lattice symbols
LATTICE_CODE = {
    'triclinic':     'a',
    'monoclinic':    'm',
    'orthorhombic':  'o',
    'tetragonal':    't',
    'rhombohedral':  'h',
    'hexagonal':     'h',
    'cubic':         'c'
}


def parse_float_from_tag(block, tag):
    """
    Extract a numeric value from a CIF tag, stripping any parentheses (uncertainty) suffix.
    """
    raw = block.find_value(tag)
    if not raw:
        raise ValueError(f"Missing CIF tag: {tag}")
    # Remove parentheses and any trailing whitespace
    num = re.sub(r"\(.*\)$", "", raw).strip()
    return float(num)


def extract_parameters(cif_path):
    """
    Parse CIF and extract lattice_type, centering, unique_axis, cell lengths and angles,
    and compute 2-letter Bravais code.
    Returns:
        dict with keys: lattice_type, centering, unique_axis, a, b, c, alpha, beta, gamma, bravais
    """
    doc = gemmi.cif.read_file(cif_path)
    block = doc.sole_block()

    # Crystal system / cell setting
    lattice_type = block.find_value('_symmetry_cell_setting').lower()

    # Hall or H-M symbol for centering, strip quotes
    raw_hm = block.find_value('_symmetry_space_group_name_H-M')
    if raw_hm:
        hm_clean = raw_hm.strip().strip("'\"")
        centering = hm_clean.split()[0].upper()
    else:
        centering = ''

    # Determine unique axis from mapping or infer for monoclinic
    unique_axis = UNIQUE_AXIS.get(lattice_type)
    if unique_axis is None:
        alpha = parse_float_from_tag(block, '_cell_angle_alpha')
        beta  = parse_float_from_tag(block, '_cell_angle_beta')
        gamma = parse_float_from_tag(block, '_cell_angle_gamma')
        unique_axis = (
            'a' if beta == 90 and gamma == 90 and alpha != 90 else
            'b' if alpha == 90 and gamma == 90 and beta != 90 else
            'c'
        )

    # Cell parameters
    a     = parse_float_from_tag(block, '_cell_length_a')
    b     = parse_float_from_tag(block, '_cell_length_b')
    c     = parse_float_from_tag(block, '_cell_length_c')
    alpha = parse_float_from_tag(block, '_cell_angle_alpha')
    beta  = parse_float_from_tag(block, '_cell_angle_beta')
    gamma = parse_float_from_tag(block, '_cell_angle_gamma')

    # Compute Bravais code: lattice letter + centering
    lat_code = LATTICE_CODE.get(lattice_type, '?')
    bravais = f"{lat_code}{centering}"

    return {
        'lattice_type': lattice_type,
        'centering':   centering,
        'unique_axis': unique_axis,
        'a': a, 'b': b, 'c': c,
        'alpha': alpha, 'beta': beta, 'gamma': gamma,
        'bravais': bravais
    }

def write_cell(params, cell_path):
    """
    Write the parameters into a CrystFEL .cell file,
    auto-selecting unique_axis based on lattice_type.
    """

    # lookup (case-insensitive) and fall back to omitting the line
    lattice = params['lattice_type'].lower()
    unique = AXIS_MAP.get(lattice)

    with open(cell_path, 'w') as f:
        f.write("CrystFEL unit cell file version 1.0\n\n")
        f.write(f"lattice_type = {params['lattice_type']}\n")
        f.write(f"centering     = {params['centering']}\n")
        if unique:
            f.write(f"unique_axis   = {unique}\n\n")
        else:
            f.write("\n")

        f.write(f"a = {params['a']:.4f} A\n")
        f.write(f"b = {params['b']:.4f} A\n")
        f.write(f"c = {params['c']:.4f} A\n")
        f.write(f"al = {params['alpha']:.2f} deg\n")
        f.write(f"be = {params['beta']:.2f} deg\n")
        f.write(f"ga = {params['gamma']:.2f} deg\n")



def main():
    parser = argparse.ArgumentParser(
        description='Convert CIF to CrystFEL .cell or output 2-letter Bravais code.'
    )
    parser.add_argument('cif', help='Input CIF file')
    parser.add_argument('-o', '--output', metavar='CELL', help='Write .cell file to this path')
    parser.add_argument('--code', action='store_true', help='Print only the 2-letter Bravais code')
    args = parser.parse_args()

    params = extract_parameters(args.cif)

    # Determine output path
    if args.output:
        cell_path = args.output
    else:
        base, _ = os.path.splitext(args.cif)
        cell_path = base + '.cell'

    # Write .cell if requested or by default
    if args.output or not args.code:
        write_cell(params, cell_path)
        print(f"Wrote: {cell_path}")

    # Print code if requested or by default
    if args.code or not args.output:
        print(params['bravais'])


if __name__ == '__main__':
    main()