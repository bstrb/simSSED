#!/usr/bin/env python
import numpy as np

##############################################################################
# A) Convert one quaternion (w, x, y, z) to a 3×3 rotation matrix
#    WITHOUT using ORIX methods.
##############################################################################
def quaternion_to_rotation_matrix(quaternion):
    """
    Convert a raw quaternion (w, x, y, z) to a 3x3 rotation matrix.

    Parameters
    ----------
    quaternion : tuple or list or np.ndarray
        The four components (w, x, y, z).
    
    Returns
    -------
    R : (3, 3) np.ndarray
        The corresponding rotation matrix.
    """
    w, x, y, z = quaternion

    # Normalize (important in case the quaternion isn't exactly unit length)
    norm = np.sqrt(w**2 + x**2 + y**2 + z**2)
    w, x, y, z = w / norm, x / norm, y / norm, z / norm

    # Construct rotation matrix from quaternion
    R = np.array([
        [1 - 2*(y**2 + z**2),   2*(x*y - w*z),       2*(x*z + w*y)],
        [2*(x*y + w*z),         1 - 2*(x**2 + z**2), 2*(y*z - w*x)],
        [2*(x*z - w*y),         2*(y*z + w*x),       1 - 2*(x**2 + y**2)]
    ], dtype=float)
    return R


##############################################################################
# B) Build the B (reciprocal-lattice) matrix from cell parameters
##############################################################################
def B_matrix_from_cell(a, b, c, alpha_deg, beta_deg, gamma_deg, use_2pi=False):
    """
    Construct the 3x3 B matrix for a cell with parameters (a, b, c, alpha, beta, gamma).
    Columns = [a*, b*, c*]. If use_2pi=True, multiply each by 2π.
    """
    alpha = np.radians(alpha_deg)
    beta  = np.radians(beta_deg)
    gamma = np.radians(gamma_deg)

    # Real-space vectors in a standard 'crystal' coordinate system
    A = np.array([a, 0.0, 0.0])
    B_ = np.array([b*np.cos(gamma), b*np.sin(gamma), 0.0])
    cx = c * np.cos(beta)
    cy = c * (np.cos(alpha) - np.cos(beta)*np.cos(gamma)) / np.sin(gamma)
    cz = np.sqrt(c**2 - cx**2 - cy**2)
    C = np.array([cx, cy, cz])

    # Volume
    V = A.dot(np.cross(B_, C))

    # Reciprocal-lattice vectors (no 2π by default)
    a_star = np.cross(B_, C) / V
    b_star = np.cross(C, A)  / V
    c_star = np.cross(A, B_) / V

    if use_2pi:
        a_star *= 2*np.pi
        b_star *= 2*np.pi
        c_star *= 2*np.pi

    return np.column_stack((a_star, b_star, c_star))


##############################################################################
# C) Compute UB for each orientation in an ORIX Rotation object
#    by extracting a,b,c,d (i.e. w,x,y,z) manually.
##############################################################################
def compute_UB_matrices_from_orix_quaternions(orientations, a, b, c,
                                              alpha, beta, gamma,
                                              use_2pi=False):
    """
    For each orientation in an ORIX Rotation object, build the UB matrix
    using a manual quaternion->rotation conversion.

    Parameters
    ----------
    orientations : orix.orientation.Rotation
        The object with shape (N,). We do NOT call .rotation_matrix().
        We read quaternion components from .a, .b, .c, .d
    a, b, c : float
        Lattice constants in Å.
    alpha, beta, gamma : float
        Lattice angles in degrees.
    use_2pi : bool
        If True, reciprocal vectors in B get multiplied by 2π.

    Returns
    -------
    UB_list : (N, 3, 3) np.ndarray
        The UB matrix for each orientation.
    """
    # 1) Build B once
    B = B_matrix_from_cell(a, b, c, alpha, beta, gamma, use_2pi=use_2pi)

    # n = len(orientations)  # e.g. 171
    n = orientations.a.shape[0]

    UB_list = np.zeros((n, 3, 3), dtype=float)

    # 2) Extract the quaternion arrays from 'orientations'
    #    Each of these is shape (N,)
    w_array = orientations.a
    x_array = orientations.b
    y_array = orientations.c
    z_array = orientations.d

    # 3) Loop over each orientation, build U, then multiply by B
    for i in range(n):
        w = w_array[i]
        x = x_array[i]
        y = y_array[i]
        z = z_array[i]

        U = quaternion_to_rotation_matrix((w, x, y, z))
        UB_list[i] = U @ B

    return UB_list


##############################################################################
# D) Example usage
##############################################################################
if __name__ == "__main__":
    
    import numpy as np
    from orix.crystal_map import Phase
    from orix.sampling import get_sample_reduced_fundamental
    from diffpy.structure import Lattice, Structure, Atom
    from parse_pdb_with_scale_remove_h import parse_pdb_with_scale

    pdbfile = "/Users/xiaodong/Desktop/simulations/UOX/UOX.pdb"

    cell, sg_sym, atoms = parse_pdb_with_scale(pdbfile, remove_hydrogens=True, include_occupancy=True)

    lattice = Lattice(*cell)

    # Define the phase using less atoms than in the pdb for computational reasons
    atoms = [Atom("C", (0, 0, 0), 1.0)]

    # Create the structure and corresponding phase
    structure = Structure(atoms, lattice)
    phase = Phase(space_group = 23, structure=structure)

    # Sample orientations in the symmetry-reduced zone (resolution in degrees)
    orientations = get_sample_reduced_fundamental(resolution=10, point_group=phase.point_group)

    # Cell parameters from your example
    # a, b, c = 80.58, 94.49, 103.89 #in Å
    a, b, c = 8.058, 9.449, 10.389 #in nm
    alpha, beta, gamma = 90.0, 90.0, 90.0
    use_2pi = True

    # Compute UB
    UB_all = compute_UB_matrices_from_orix_quaternions(
        orientations, a, b, c, alpha, beta, gamma, use_2pi=use_2pi
    )


    # # Write UB matrices to a .sol file
    with open("/Users/xiaodong/Desktop/simulations/UOX/UB_matrices.sol", "w") as sol_file:
        for i, matrix in enumerate(UB_all):
            # Flatten the 3x3 matrix (row-major order)
            # Each number is formatted with a sign (+ or -) and 7 decimal places.
            line = " ".join(f"{num:+.7f}" for num in matrix.flatten())
            sol_file.write(f"/Users/xiaodong/Desktop/simulations/UOX/simulation-30/sim.h5 //{i} " + line + " 0.000 0.000 oI\n")




