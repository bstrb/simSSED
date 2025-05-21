#!/usr/bin/env python

from diffpy.structure import Atom

def parse_pdb_with_scale(pdbfile, remove_hydrogens=False, include_occupancy=True):
    """
    Parse a PDB file manually:
      - CRYST1  : cell parameters + space group
      - SCALE1-3: 3x3 + translation for coordinate transform
      - ATOM    : x, y, z, occupancy, element

    Parameters
    ----------
    pdbfile : str
        Path to the PDB file to parse.
    remove_hydrogens : bool, optional
        If True, skip (do not add) any atom whose element is hydrogen
        (i.e., element.strip().upper().startswith('H')). Default is False.
    include_occupancy : bool, optional
        If True, read occupancy from PDB file. If False, set occupancy=1.0
        for all atoms. Default is True.

    Returns
    -------
    cell : tuple or None
        Tuple of (a, b, c, alpha, beta, gamma). None if no CRYST1 found.
    space_group_symbol : str or None
        Space group string from the CRYST1 record (with spaces removed).
    atom_list : list of diffpy.structure.Atom
        List of Atom objects with fractional coordinates from the scale matrix.
    """

    # -----------------------
    # 1) Initialize defaults
    # -----------------------
    a = b = c = alpha = beta = gamma = None
    space_group_symbol = None

    # Default scale matrix = identity (if no SCALE lines found)
    scale = [
        [1.0, 0.0, 0.0, 0.0],  # row for x'
        [0.0, 1.0, 0.0, 0.0],  # row for y'
        [0.0, 0.0, 1.0, 0.0],  # row for z'
    ]

    # We'll collect atoms in a list
    atom_list = []

    # ---------------------------------------------------
    # 2) Read file line by line, parse CRYST1, SCALE1-3, ATOM
    # ---------------------------------------------------
    with open(pdbfile, 'r') as f:
        for line in f:
            line_id = line[0:6].strip()

            # CRYST1 record -> cell parameters & space group
            if line_id == 'CRYST1':
                # Usually columns:
                #  7 - 15 : a
                # 16 - 24 : b
                # 25 - 33 : c
                # 34 - 40 : alpha
                # 41 - 47 : beta
                # 48 - 54 : gamma
                # 56 - 66 : space group
                a     = float(line[6:15])
                b     = float(line[15:24])
                c     = float(line[24:33])
                alpha = float(line[33:40])
                beta  = float(line[40:47])
                gamma = float(line[47:54])
                sg    = line[55:66].strip()  # e.g. "I 2 2 2"
                space_group_symbol = sg.replace(" ", "")

            # SCALEn lines -> fill in the scale matrix row by row
            elif line_id.startswith('SCALE'):
                row_index = int(line_id[-1]) - 1  # 'SCALE1' -> row=0, 'SCALE2'-> row=1, etc.
                s0 = float(line[10:20])
                s1 = float(line[20:30])
                s2 = float(line[30:40])
                s3 = float(line[45:55])
                scale[row_index] = [s0, s1, s2, s3]

            # ATOM lines -> read x, y, z, occupancy, element
            elif line_id == 'ATOM':
                # Standard PDB columns:
                # 30-38: x
                # 38-46: y
                # 46-54: z
                # 54-60: occupancy
                # 76-78: element
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                if include_occupancy:
                    occ = float(line[54:60])
                else:
                    occ = 1.0

                element = str(line[76:78].strip())  # e.g. "C", "N", "O", "FE", etc.

                # Optionally skip hydrogen atoms
                if remove_hydrogens and element.upper().startswith('H'):
                    continue

                # Apply the scale transform
                xprime = scale[0][0]*x + scale[0][1]*y + scale[0][2]*z + scale[0][3]
                yprime = scale[1][0]*x + scale[1][1]*y + scale[1][2]*z + scale[1][3]
                zprime = scale[2][0]*x + scale[2][1]*y + scale[2][2]*z + scale[2][3]

                # Create a Diffpy Atom with fractional coords
                atom = Atom(element, xyz=(xprime, yprime, zprime), occupancy=occ)
                atom_list.append(atom)

    # -------------------------------------------------------
    # 3) Create the Lattice & Structure if we have CRYST1 data
    # -------------------------------------------------------
    cell = (a, b, c, alpha, beta, gamma)

    return cell, space_group_symbol, atom_list


# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    import sys

    # Provide your PDB file path
    pdbfile = "/Users/xiaodong/Desktop/simserialED-main/UOX.pdb"

    # 1) Default parse (include hydrogens, include occupancy)
    cell, sg_sym, atoms = parse_pdb_with_scale(pdbfile)
    print("Parsed space group:", sg_sym)
    print("Cell:", cell)
    print("Number of atoms:", len(atoms))

    # 2) Remove hydrogens, keep occupancy
    cell_noH_occ, sg_sym_noH_occ, atoms_noH_occ = parse_pdb_with_scale(
        pdbfile, remove_hydrogens=True, include_occupancy=True
    )
    print("\nParsed with no hydrogens (occupancy included):")
    print("Parsed space group:", sg_sym_noH_occ)
    print("Cell:", cell_noH_occ)
    print("Number of atoms:", len(atoms_noH_occ))

    # 3) Keep hydrogens, but do NOT include occupancy from file
    cell_H_noOcc, sg_sym_H_noOcc, atoms_H_noOcc = parse_pdb_with_scale(
        pdbfile, remove_hydrogens=False, include_occupancy=False
    )
    print("\nParsed with hydrogens (occupancy forced to 1.0):")
    print("Parsed space group:", sg_sym_H_noOcc)
    print("Cell:", cell_H_noOcc)
    print("Number of atoms:", len(atoms_H_noOcc))
