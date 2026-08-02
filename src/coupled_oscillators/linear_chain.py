"""Finite linear chains mechanics."""
import numpy as np
from typing import Tuple

def build_k_matrix(N: int, k: float = 1.0, boundary: str = "fixed") -> np.ndarray:
    """Construct stiffness (K) matrix for N masses."""
    K = np.zeros((N, N))
    for i in range(N):
        K[i, i] = 2 * k
        if i > 0:
            K[i, i-1] = -k
        if i < N - 1:
            K[i, i+1] = -k
            
    if boundary == "free":
        K[0, 0] = k
        K[-1, -1] = k
    elif boundary == "periodic":
        if N > 2:
            K[0, -1] = -k
            K[-1, 0] = -k
    return K

def build_mass_matrix(N: int, m: float = 1.0) -> np.ndarray:
    """Construct mass matrix for N masses."""
    return np.eye(N) * m

def solve_eigensystem(K: np.ndarray, M: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
    """Generalized eigenproblem Kx = omega^2 Mx."""
    if M is None:
        M = np.eye(K.shape[0])
    from scipy.linalg import eigh
    evals, evecs = eigh(K, M)
    return sort_modes(evals, evecs)

def analytical_omegas_fixed(N: int, k: float = 1.0, m: float = 1.0) -> np.ndarray:
    """Compute closed-form normal-mode frequencies for fixed-end chain."""
    j = np.arange(1, N + 1)
    return 2 * np.sqrt(k / m) * np.sin(j * np.pi / (2 * (N + 1)))

def normalize_modes(evecs: np.ndarray) -> np.ndarray:
    """Ensure eigenvectors are orthonormal (unit length)."""
    norms = np.linalg.norm(evecs, axis=0)
    return evecs / norms

def sort_modes(evals: np.ndarray, evecs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Sort eigenvalues & eigenvectors in ascending omega."""
    idx = np.argsort(evals)
    return evals[idx], evecs[:, idx]
