import numpy as np

def calculate_calibration(
    wavelength_A=0.0251,
    clen_m=1.885,
    res=17857.14285714286  # 56 µm pixel size implies 1/res ≈ 56e-6 m
):
    """
    Compute both the reciprocal-space calibration (1/Å per pixel) and 
    the scattering vector q (1/Å per pixel) based on geometry.

    :param wavelength_A: X-ray or electron wavelength in Å
    :param clen_m:       Camera length in meters
    :param res:          Pixel resolution (pixels per meter) = 1 / (pixel size in meters)
    :return:             tuple of (calibration in 1/Å per pixel, q in 1/Å per pixel)
    """
    # Convert wavelength to meters
    lambda_m = wavelength_A * 1e-10  # 1 Å = 1e-10 m

    # Compute pixel size in meters
    pixel_size_m = 1.0 / res  # meters per pixel

    # Calculate d-spacing in meters for a diffraction spot at 1 pixel distance
    theta = np.arctan(pixel_size_m / clen_m)
    d_m = lambda_m / (2 * np.sin(theta))

    # Convert d from meters to Ångstroms
    d_A = d_m * 1e10

    # Compute calibration as reciprocal of d in 1/Å
    calibration = 1.0 / (2*d_A)


    print("Calibration (1/Å per pixel) =", calibration)

    return calibration

# Example usage:
if __name__ == "__main__":
    # Define experimental parameters:
    wavelength_A = 0.0251                 # Cu Kα X-ray wavelength in Å
    camera_length_m = 1.0                   # camera length in meters
    pixel_resolution = 17857.14285714286    #  1.0 / 55e-6  # Example: 55 µm pixel size -> pixels per meter


    # Call the function with these parameters
    calibration_value = calculate_calibration(
        wavelength_A, camera_length_m, pixel_resolution
    )

    print(f"Calculated calibration: {calibration_value:.4f} 1/Å per pixel")
