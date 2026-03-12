\
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from cred_sim.xds import load_xds_geometry

def main():
    ap = argparse.ArgumentParser(description="Print the minimal geometry parsed from XDS.")
    ap.add_argument("--xds", required=True, help="Path to XDS folder")
    args = ap.parse_args()

    geom = load_xds_geometry(args.xds)
    print(geom)

if __name__ == "__main__":
    main()
