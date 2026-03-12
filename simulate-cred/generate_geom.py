#!/usr/bin/env python3
import argparse
import textwrap


def generate_geom_text(
    wavelength: float = 0.019687,
    adu: float = 5,
    clen: float = 0.3,
    res: float = 17857.14285714286,
    corner_x: float = -512.5,
    corner_y: float = -512.5,
) -> str:
    """
    Generate the content of a .geom file based on provided parameters.

    Parameters:
        wavelength: Wavelength in Å (default 0.019687)
        adu: ADU per photon (default 5)
        clen: Camera length in meters (default 0.3)
        res: Resolution (default 17857.14285714286)
        corner_x: Detector corner X (default -512.5)
        corner_y: Detector corner Y (default -512.5)

    Returns:
        A string containing the formatted .geom content.
    """
    return textwrap.dedent(f"""\
        wavelength  = {wavelength} A
        adu_per_photon = {adu}
        clen = {clen} m

        res = {res}
        data = /entry/data/images
        dim0 = %
        dim1 = ss
        dim2 = fs
        detector_shift_x = /entry/data/det_shift_x_mm mm
        detector_shift_y = /entry/data/det_shift_y_mm mm
        p0/min_ss = 0
        p0/max_ss = 1023
        p0/min_fs = 0
        p0/max_fs = 1023
        p0/corner_x = {corner_x}
        p0/corner_y = {corner_y}
        p0/fs = x
        p0/ss = y
    """)


def write_geom_file(
    filename: str,
    wavelength: float = 0.019687,
    adu: float = 5,
    clen: float = 0.3,
    res: float = 17857.14285714286,
    corner_x: float = -512.5,
    corner_y: float = -512.5,
) -> None:
    """
    Write the .geom file with given parameters to the specified filename.
    """
    content = generate_geom_text(
        wavelength, adu, clen, res, corner_x, corner_y
    )
    with open(filename, "w") as f:
        f.write(content)
    print(f"→ Wrote {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a .geom file with specified parameters (importable API and CLI)"
    )
    parser.add_argument(
        "--wavelength", type=float, default=0.019687,
        help="Wavelength in Å (default: 0.019687)"
    )
    parser.add_argument(
        "--adu", type=float, default=5,
        help="ADU per photon (default: 5)"
    )
    parser.add_argument(
        "--clen", type=float, default=0.3,
        help="Camera length in meters (default: 0.3)"
    )
    parser.add_argument(
        "--res", type=float, default=17857.14285714286,
        help="Resolution (default: 17857.14285714286)"
    )
    parser.add_argument(
        "--corner_x", type=float, default=-512.5,
        help="Detector corner X (default: -512.5)"
    )
    parser.add_argument(
        "--corner_y", type=float, default=-512.5,
        help="Detector corner Y (default: -512.5)"
    )
    parser.add_argument(
        "--output", "-o", default="output.geom",
        help="Output filename (default: output.geom)"
    )

    args = parser.parse_args()
    write_geom_file(
        filename=args.output,
        wavelength=args.wavelength,
        adu=args.adu,
        clen=args.clen,
        res=args.res,
        corner_x=args.corner_x,
        corner_y=args.corner_y,
    )


if __name__ == "__main__":
    main()
