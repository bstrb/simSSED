\
"""
Plotting utilities for simulated patterns and overlays.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def show_pattern(img: np.ndarray, title: str = "", vmin: Optional[float] = None, vmax: Optional[float] = None):
    plt.figure()
    plt.imshow(img, cmap="gray", origin="lower", vmin=vmin, vmax=vmax)
    plt.title(title)
    plt.xlabel("x (px)")
    plt.ylabel("y (px)")
    plt.tight_layout()

def overlay_spots(img: np.ndarray, spots: pd.DataFrame, title: str = "", spot_size: float = 10.0,
                  vmin: Optional[float] = None, vmax: Optional[float] = None):
    plt.figure()
    plt.imshow(img, cmap="gray", origin="lower", vmin=vmin, vmax=vmax)
    if len(spots):
        plt.scatter(spots["x_px"], spots["y_px"], s=spot_size, facecolors="none", edgecolors="r", linewidths=1.0)
    plt.title(title)
    plt.xlabel("x (px)")
    plt.ylabel("y (px)")
    plt.tight_layout()
