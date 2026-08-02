import os
import scipy.constants as const

files = {}

files["src/coupled_oscillators/constants.py"] = '''\
"\""Physical constants for the Coupled Oscillators project."\""
import scipy.constants as const

MU_0 = const.mu_0  # Vacuum permeability
GAMMA = 1.760859644e11  # Gyromagnetic ratio for electron (rad s^-1 T^-1)
'''

files["src/coupled_oscillators/validation.py"] = '''\
"\""Physics validation and check routines."\""
import numpy as np

def check_symmetric(matrix: np.ndarray, tol: float = 1e-10) -> bool:
    "\""Check if a matrix is symmetric."\""
    if not np.allclose(matrix, matrix.T, atol=tol):
        raise ValueError("Matrix is not symmetric.")
    return True

def check_positive_eigs(evals: np.ndarray) -> bool:
    "\""Check if all eigenvalues are non-negative (within tolerance)."\""
    if np.any(evals < -1e-10):
        raise ValueError(f"Found negative eigenvalues: {evals[evals < -1e-10]}")
    return True

def check_energy_conservation(energies: np.ndarray, tol: float = 1e-5) -> bool:
    "\""Check if energy is conserved over time."\""
    E0 = energies[0]
    if not np.allclose(energies, E0, rtol=tol, atol=tol):
        raise ValueError("Energy is not conserved over the time series.")
    return True
'''

files["src/coupled_oscillators/plotting.py"] = '''\
"\""Consistent plotting style and helpers for the project."\""
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional

# Set consistent plotting style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 12

def plot_time_series(t: np.ndarray, x: np.ndarray, labels: Optional[List[str]] = None, title: str = "Time Series"):
    "\""Plot time series of displacements or other variables."\""
    fig, ax = plt.subplots(figsize=(8, 5))
    if x.ndim == 1:
        ax.plot(t, x, label=labels[0] if labels else None)
    else:
        for i in range(x.shape[1]):
            label = labels[i] if labels and i < len(labels) else f"Node {i}"
            ax.plot(t, x[:, i], label=label)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    if labels or x.ndim > 1:
        ax.legend()
    plt.tight_layout()
    return fig, ax

def plot_phase_space(x: np.ndarray, v: np.ndarray, title: str = "Phase Space"):
    "\""Plot phase space (x vs v)."\""
    fig, ax = plt.subplots(figsize=(6, 6))
    if x.ndim == 1:
        ax.plot(x, v)
    else:
        for i in range(x.shape[1]):
            ax.plot(x[:, i], v[:, i], label=f"Node {i}")
        ax.legend()
    ax.set_xlabel("Position (x)")
    ax.set_ylabel("Velocity (v)")
    ax.set_title(title)
    plt.tight_layout()
    return fig, ax

def plot_mode_shapes(modes: np.ndarray, node_positions: Optional[np.ndarray] = None, title: str = "Mode Shapes"):
    "\""Plot the mode shapes. modes should be a 2D array where columns are eigenvectors."\""
    N = modes.shape[0]
    if node_positions is None:
        node_positions = np.arange(N)
        
    fig, ax = plt.subplots(figsize=(8, 5))
    for i in range(modes.shape[1]):
        ax.plot(node_positions, modes[:, i], marker='o', label=f"Mode {i}")
    ax.set_xlabel("Node Position")
    ax.set_ylabel("Displacement Amplitude")
    ax.set_title(title)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig, ax

def plot_dispersion(k: np.ndarray, omega: np.ndarray, title: str = "Dispersion Relation"):
    "\""Plot dispersion relation ? vs k."\""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(k, omega, 'b-', lw=2)
    ax.set_xlabel("Wavevector (k)")
    ax.set_ylabel("Angular Frequency (?)")
    ax.set_title(title)
    plt.tight_layout()
    return fig, ax
'''

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
