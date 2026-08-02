"""Physics validation and check routines."""
import numpy as np

def check_symmetric(matrix: np.ndarray, tol: float = 1e-10) -> bool:
    """Check if a matrix is symmetric."""
    if not np.allclose(matrix, matrix.T, atol=tol):
        raise ValueError("Matrix is not symmetric.")
    return True

def check_positive_eigs(evals: np.ndarray) -> bool:
    """Check if all eigenvalues are non-negative (within tolerance)."""
    if np.any(evals < -1e-10):
        raise ValueError(f"Found negative eigenvalues: {evals[evals < -1e-10]}")
    return True

def check_energy_conservation(energies: np.ndarray, tol: float = 1e-5) -> bool:
    """Check if energy is conserved over time."""
    E0 = energies[0]
    if not np.allclose(energies, E0, rtol=tol, atol=tol):
        raise ValueError("Energy is not conserved over the time series.")
    return True
