"""Modal projection and reconstruction."""
import numpy as np

def project_initial_condition(x0: np.ndarray, modes: np.ndarray) -> np.ndarray:
    """Compute modal coefficients a_j = V_j dot x0."""
    return modes.T @ x0

def reconstruct_state(modes: np.ndarray, coeffs: np.ndarray, omega: np.ndarray, t: float) -> np.ndarray:
    """Compute displacement x(t) = Sum a_j cos(omega_j t) V_j."""
    time_evolution = coeffs * np.cos(omega * t)
    return modes @ time_evolution

def mode_overlap_matrix(modes: np.ndarray) -> np.ndarray:
    """Compute V^T V."""
    return modes.T @ modes

def check_orthogonality(modes: np.ndarray, tol: float = 1e-10) -> bool:
    """Verify V^T V is identity to tolerance."""
    overlap = mode_overlap_matrix(modes)
    I = np.eye(modes.shape[1])
    return np.allclose(overlap, I, atol=tol)

def check_completeness(modes: np.ndarray, tol: float = 1e-10) -> bool:
    """Verify V V^T is identity to tolerance."""
    completeness_mat = modes @ modes.T
    I = np.eye(modes.shape[0])
    return np.allclose(completeness_mat, I, atol=tol)

def modal_energy(x: np.ndarray, v: np.ndarray, modes: np.ndarray, omega: np.ndarray, m: float = 1.0) -> np.ndarray:
    """Compute energy in each mode given displacements and velocities."""
    q = modes.T @ x
    q_dot = modes.T @ v
    return 0.5 * m * (q_dot**2 + (omega**2) * (q**2))
