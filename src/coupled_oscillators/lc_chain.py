"""Electrical analogues (LC oscillators)."""
import numpy as np

def build_lc_matrix(N: int, L: float = 1.0, C: float = 1.0, Cc: float = 0.0) -> np.ndarray:
    """Stiffness matrix for LC ladder with coupling Cc."""
    K = np.zeros((N, N))
    for i in range(N):
        K[i, i] = 1.0 / (L * C) + 2.0 * Cc / (L * C)
        if i > 0:
            K[i, i-1] = -Cc / (L * C)
        if i < N - 1:
            K[i, i+1] = -Cc / (L * C)
    return K

def single_lc_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    """ODE for single LC oscillator (charge/flux). y = [q, i]"""
    q, i = y
    L = params.get("L", 1.0)
    C = params.get("C", 1.0)
    return np.array([i, -q / (L * C)])

def coupled_lc_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    """ODEs for two coupled LC circuits."""
    q1, i1, q2, i2 = y
    L = params.get("L", 1.0)
    C = params.get("C", 1.0)
    Cc = params.get("Cc", 0.1)
    
    dq1_dt = i1
    di1_dt = -(q1 + Cc*(q1-q2)) / (L * C)
    dq2_dt = i2
    di2_dt = -(q2 + Cc*(q2-q1)) / (L * C)
    return np.array([dq1_dt, di1_dt, dq2_dt, di2_dt])

def lc_dispersion(k: np.ndarray, L: float, C: float, Cc: float) -> np.ndarray:
    """Analytical omega(k) for infinite LC line."""
    return np.sqrt(1/(L*C) + (4*Cc/(L*C)) * np.sin(k/2)**2)

def lc_cutoff_frequency(L: float, C: float) -> float:
    """omega_cutoff = 1/sqrt(LC)."""
    return 1.0 / np.sqrt(L * C)

def compare_lc_mechanical(omega_lc: np.ndarray, omega_mech: np.ndarray) -> float:
    """Utility to compare LC and mass-spring spectra (returns max difference)."""
    return np.max(np.abs(omega_lc - omega_mech))
