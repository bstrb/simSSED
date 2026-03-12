\
"""
Image I/O helpers.

Supports:
- SMV (.img) common in XDS workflows
- MRC (.mrc / .mrcs)
- common image formats supported by imageio (png, tif, etc.)

This stays minimal and does not attempt to cover every detector format.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple, Dict, Any

import numpy as np

def read_smv(path: str | Path) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Minimal SMV reader for unsigned short / signed short / int32 images.

    Many SMV files have a text header enclosed in '{...}' and specify:
      HEADER_BYTES, SIZE1, SIZE2, BYTE_ORDER, TYPE or DATA_TYPE

    Returns (image, header_dict).
    """
    path = Path(path)
    with path.open("rb") as fh:
        raw = fh.read()

    # Header is ASCII within first HEADER_BYTES; we find closing brace.
    end = raw.find(b"}")
    if end == -1:
        raise ValueError(f"Could not find SMV header end '}}' in {path}")
    header_text = raw[:end+1].decode("ascii", errors="replace")

    # Parse key/value pairs like "KEY=VALUE;"
    header: Dict[str, Any] = {}
    # Remove braces
    ht = header_text.strip().lstrip("{").rstrip("}")
    for item in ht.split(";"):
        item = item.strip()
        if not item or "=" not in item:
            continue
        k, v = item.split("=", 1)
        header[k.strip()] = v.strip()

    header_bytes = int(header.get("HEADER_BYTES", 512))
    size1 = int(header.get("SIZE1", header.get("DIM", 0) or 0))
    size2 = int(header.get("SIZE2", header.get("DIM", 0) or 0))
    if size1 <= 0 or size2 <= 0:
        # Some detectors use NFAST/NSLOW
        size1 = int(header.get("NFAST", 0) or 0)
        size2 = int(header.get("NSLOW", 0) or 0)
    if size1 <= 0 or size2 <= 0:
        raise ValueError(f"Could not determine SIZE1/SIZE2 in SMV header for {path}")

    byte_order = header.get("BYTE_ORDER", "little_endian").lower()
    endian = "<" if "little" in byte_order else ">"

    # Data type
    data_type = header.get("TYPE", header.get("DATA_TYPE", "unsigned_short")).lower()
    if "unsigned_short" in data_type or "uint16" in data_type:
        dtype = np.dtype(endian + "u2")
    elif "signed_short" in data_type or "int16" in data_type:
        dtype = np.dtype(endian + "i2")
    elif "int" in data_type or "integer" in data_type or "int32" in data_type:
        dtype = np.dtype(endian + "i4")
    elif "float" in data_type:
        dtype = np.dtype(endian + "f4")
    else:
        raise ValueError(f"Unsupported SMV data type '{data_type}' in {path}")

    data = np.frombuffer(raw, dtype=dtype, offset=header_bytes, count=size1*size2)
    img = data.reshape((size2, size1)).astype(np.float32)
    return img, header

def read_mrc(path: str | Path) -> np.ndarray:
    import mrcfile
    with mrcfile.open(str(path), permissive=True) as mrc:
        arr = mrc.data.copy()
    # Ensure 2D
    if arr.ndim == 3:
        # Take first slice
        arr = arr[0]
    return arr.astype(np.float32)

def read_image(path: str | Path) -> np.ndarray:
    path = Path(path)
    suf = path.suffix.lower()
    if suf in (".img", ".smv"):
        img, _ = read_smv(path)
        return img
    if suf in (".mrc", ".mrcs"):
        return read_mrc(path)
    # fallback: imageio
    import imageio.v2 as imageio
    img = imageio.imread(path)
    return np.asarray(img, dtype=np.float32)
