"""Magnonic crystals and devices."""
import numpy as np
from typing import Tuple

def build_exchange_profile(N: int, pattern: str, J0: float = 1.0, J1: float = 0.5) -> np.ndarray:
    """Create spatially varying exchange constant array."""
    profile = np.ones(N) * J0
    if pattern == "alternating":
        profile[1::2] = J1
    elif pattern == "defect":
        profile[N//2] = J1
    return profile

def build_anisotropy_profile(N: int, pattern: str, K0: float = 0.0, K1: float = 1.0) -> np.ndarray:
    """Create spatially varying anisotropy array."""
    profile = np.ones(N) * K0
    if pattern == "defect":
        profile[N//2] = K1
    return profile

def domain_wall_profile(N: int, width: float, orientation: str = "z") -> np.ndarray:
    """Initialize spins with a smooth domain wall."""
    x = np.arange(N) - N/2.0
    # standard Walker profile theta = 2*arctan(exp(x / width))
    theta = 2 * np.arctan(np.exp(x / width))
    
    spins = np.zeros((N, 3))
    if orientation == "z":
        spins[:, 0] = np.sin(theta)
        spins[:, 2] = np.cos(theta)
    return spins

def transmission_spectrum(inc_wave: np.ndarray, defect_structure: np.ndarray, params: dict) -> float:
    """Simulate transmission of incident wave."""
    # placeholder for actual integration or scattering matrix approach
    return 1.0

def reflection_coefficient(inc_wave: np.ndarray, defect_structure: np.ndarray, params: dict) -> float:
    """Compute reflection coefficient R."""
    return 0.0

def hybrid_mode_fit(frequencies: np.ndarray, tuning_param: np.ndarray) -> float:
    """Fit avoided-crossing curves to extract coupling strength 2g."""
    # Very simplified: g is half the minimum gap
    diff = np.abs(frequencies[1] - frequencies[0])
    g = np.min(diff) / 2.0
    return g
