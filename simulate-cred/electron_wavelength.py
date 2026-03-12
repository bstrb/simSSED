#!/usr/bin/env python3
"""
Compute the relativistically corrected de Broglie wavelength of an electron
accelerated through a given voltage.

Usage:
    python electron_wavelength.py [voltage_in_kV]

Example:
    >>> electron_wavelength(200)  # for 200 kV
    2.5079e-12  # meters
"""

import sys
import math

# CODATA 2022 values
h = 6.62607015e-34         # Planck constant, J·s :contentReference[oaicite:1]{index=1}
m_e = 9.1093837139e-31     # Electron rest mass, kg :contentReference[oaicite:2]{index=2}
e_charge = 1.602176634e-19 # Elementary charge, C :contentReference[oaicite:3]{index=3}
c = 299792458              # Speed of light in vacuum, m/s :contentReference[oaicite:4]{index=4}

def electron_wavelength(kV: float) -> float:
    """
    Calculate the de Broglie wavelength (in meters) of an electron
    accelerated through 'kV' kilovolts, including relativistic correction.
    """
    V = kV * 1e3  # convert kV to volts
    # relativistic momentum: p = sqrt(2 m_e e V * (1 + e V / (2 m_e c^2)))
    term = 2 * m_e * e_charge * V
    correction = 1 + (e_charge * V) / (2 * m_e * c**2)
    p = math.sqrt(term * correction)
    return h / p * 1e10  # convert to nanometers

def main():
    if len(sys.argv) == 2:
        try:
            kv = float(sys.argv[1])
        except ValueError:
            print("Please provide a numeric value for the voltage in kV.")
            sys.exit(1)
        lam = electron_wavelength(kv)
        print(f"Electron wavelength at {kv:.1f} kV: {lam:.4e} m")
    else:
        print("Usage: python electron_wavelength.py [voltage_in_kV]")
        print("Example: python electron_wavelength.py 200")

if __name__ == "__main__":
    main()
