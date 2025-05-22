import math

# your constants
WAVELENGTH_A = 0.019687            # Å
PIXELS_PER_M = 17_857.14285714286  # px · m⁻¹  (→ 56 µm px⁻¹)
N_EDGE = 1024 / 2
                     # example frame size
def clen_for_dmin(d_min_A,
                  n_pix=N_EDGE,
                  wavelength_A=WAVELENGTH_A,
                  pixels_per_m=PIXELS_PER_M):
    """
    Inverse of d_min():  return camera length L (metres) that
    gives the desired d_min (Å) at radius n_pix (pixels).

    Parameters
    ----------
    n_pix        : pixel radius from the beam centre to the spot
    d_min_A      : target highest resolution in Å
    wavelength_A : beam wavelength in Å (default: 300 kV electrons)
    pixels_per_m : detector sampling in px · m⁻¹

    Returns
    -------
    L in metres
    """
    # Å → m where necessary
    λ_m  = wavelength_A * 1e-10
    d_m  = d_min_A    * 1e-10

    # Bragg:  sinθ = λ / (2d)
    θ_max = math.asin(λ_m / (2 * d_m))
    twoθ  = 2 * θ_max

    # detector radius in metres
    R = n_pix / pixels_per_m

    # geometry:  tan(2θ) = R / L  →  L = R / tan(2θ)
    return R / math.tan(twoθ)

if __name__ == "__main__":
    # example d_min
    d_min_A = 0.3

    # calculate camera length
    L_m = clen_for_dmin(d_min_A)
    print(f"Camera length for d_min {d_min_A:.3f} Å at {N_EDGE} px: {L_m:.3f} m")
