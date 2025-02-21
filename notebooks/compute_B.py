import numpy as np

def compute_B(cell):
    """
    Given cell parameters (a, b, c, alpha, beta, gamma) where
    alpha, beta, gamma are in degrees, compute the B matrix.
    """
    a, b, c, alpha_deg, beta_deg, gamma_deg = cell
    a = a/10
    b = b/10
    c = c/10
 
    # Convert angles to radians
    alpha = np.deg2rad(alpha_deg)
    beta  = np.deg2rad(beta_deg)
    gamma = np.deg2rad(gamma_deg)

    # Compute cosine and sine of angles
    cos_alpha = np.cos(alpha)
    cos_beta  = np.cos(beta)
    cos_gamma = np.cos(gamma)
    sin_gamma = np.sin(gamma)

    # Calculate the unit cell volume:
    volume = a * b * c * np.sqrt(
        1 - cos_alpha**2 - cos_beta**2 - cos_gamma**2 + 
        2*cos_alpha*cos_beta*cos_gamma
    )

    # Construct the direct-space matrix A that transforms fractional
    # coordinates to Cartesian coordinates.
    A = np.array([
        [a,          b * cos_gamma,                    c * cos_beta],
        [0,          b * sin_gamma,                    c * (cos_alpha - cos_beta * cos_gamma) / sin_gamma],
        [0,          0,                                volume / (a * b * sin_gamma)]
    ])

    # The B matrix (mapping fractional to reciprocal space) is the inverse-transpose of A:
    B = np.linalg.inv(A).T
    return B
