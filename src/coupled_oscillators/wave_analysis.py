"""Infinite-chain and wave packets."""
import numpy as np

def dispersion_relation(k: np.ndarray, a: float, k_spring: float, m: float) -> np.ndarray:
    """omega(k) = 2*sqrt(k_spring/m)*abs(sin(ka/2))."""
    return 2 * np.sqrt(k_spring / m) * np.abs(np.sin(k * a / 2))

def phase_velocity(omega: np.ndarray, k: np.ndarray) -> np.ndarray:
    """omega/k for k>0."""
    v_p = np.zeros_like(omega)
    mask = k != 0
    v_p[mask] = omega[mask] / k[mask]
    return v_p

def group_velocity(omega_k: np.ndarray, k_grid: np.ndarray) -> np.ndarray:
    """Compute d_omega/d_k using finite differences."""
    return np.gradient(omega_k, k_grid)

def build_wave_packet(k0: float, sigma_k: float, x_grid: np.ndarray) -> np.ndarray:
    """Construct initial displacement as a Gaussian-weighted superposition around k0."""
    envelope = np.exp(- (x_grid - np.mean(x_grid))**2 / (2 * (1/sigma_k)**2))
    return envelope * np.cos(k0 * x_grid)

def fft_mode_spectrum(signal: np.ndarray, dt: float) -> tuple:
    """Compute frequency spectrum of a time-series signal."""
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=dt)
    spectrum = np.abs(np.fft.rfft(signal))
    return freqs, spectrum
