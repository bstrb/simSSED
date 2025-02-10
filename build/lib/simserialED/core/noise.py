from typing import Callable

import numpy as np

def generate_noise_pattern(
    shape: tuple[int, int],
    radial_profile: Callable[[np.ndarray], np.ndarray],
    center: tuple[int, int],
    random_seed: int = None,
    num_samples: int = None
) -> np.ndarray:
    """Sample a radial noise distribution

    Parameters
    ----------
    shape : tuple[int, int]
        Output shape
    radial_profile : Callable[[np.ndarray], np.ndarray]
        Normalized radial probability density, takes pixel distance from center as input
    center : tuple[int, int]
        Center of distribution
    random_seed : int, optional
        For rng reproducibility. Random if None, by default None
    num_samples : int, optional
        Number of samples to pull from the distribution. If None, pulls 20x the number of requested pixels, by default None

    Returns
    -------
    np.ndarray
        Noise pattern
    """
    if num_samples is None:
        num_samples = shape[0] * shape[1] * 20
    assert num_samples > 0, "Number of samples must be positive"
    
    rng = np.random.default_rng(random_seed)
    x, y = np.meshgrid(
        np.arange(shape[0]) - center[0],
        np.arange(shape[1]) - center[1],
    )
    r = (x**2 + y**2)**0.5
    density = radial_profile(r)

    out = np.zeros(shape)
    for ind in rng.choice(density.size, num_samples, p=density.flat, shuffle=False):
        out[np.unravel_index(ind, shape)] += 1
    return out
