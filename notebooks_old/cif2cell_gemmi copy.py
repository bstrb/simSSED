#!/usr/bin/env python3
"""
cif2cell_gemmi.py

Read a CIF file and write a CrystFEL .cell file (version 1.0) using Gemmi.

Usage:
    python3 cif2cell_gemmi.py input.cif output.cell

Requires:
    pip install gemmi
"""
import sys
import re
import gemmi

# Conventional unique axis mapping by crystal system
UNIQUE_AXIS = {
    'triclinic':     None,
    'monoclinic':    'b',
    'orthorhombic':  None,
    'tetragonal':    'c',
    'rhombohedral':  'c',
    'hexagonal':     'c'
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
    Parse CIF and extract lattice_type, centering, unique_axis, cell lengths and angles.
    """
    doc = gemmi.cif.read_file(cif_path)
    block = doc.sole_block()

    # Crystal system / cell setting
    lattice_type = block.find_value('_symmetry_cell_setting').lower()

    # Hall or H-M symbol for centering, strip quotes
    raw_hm = block.find_value('_symmetry_space_group_name_H-M')
    if raw_hm:
        hm_clean = raw_hm.strip().strip("'\"")
        centering = hm_clean.split()[0]
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

    return {
        'lattice_type': lattice_type,
        'centering':   centering,
        'unique_axis': unique_axis,
        'a': a, 'b': b, 'c': c,
        'alpha': alpha, 'beta': beta, 'gamma': gamma
    }


def write_cell(params, cell_path):
    """
    Write the parameters into a CrystFEL .cell file.
    """
    with open(cell_path, 'w') as f:
        f.write("CrystFEL unit cell file version 1.0\n\n")
        f.write(f"lattice_type = {params['lattice_type']}\n")
        f.write(f"centering = {params['centering']}\n")
        f.write(f"unique_axis = {params['unique_axis']}\n\n")
        f.write(f"a = {params['a']:.4f} A\n")
        f.write(f"b = {params['b']:.4f} A\n")
        f.write(f"c = {params['c']:.4f} A\n")
        f.write(f"al = {params['alpha']:.2f} deg\n")
        f.write(f"be = {params['beta']:.2f} deg\n")
        f.write(f"ga = {params['gamma']:.2f} deg\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 cif2cell_gemmi.py input.cif output.cell")
        sys.exit(1)
    input_cif   = sys.argv[1]
    output_cell = sys.argv[2]
    params = extract_parameters(input_cif)
    write_cell(params, output_cell)
    print(f"Wrote: {output_cell}")


if __name__ == '__main__':
    main()