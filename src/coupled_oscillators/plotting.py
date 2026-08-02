"""Consistent plotting style and helpers for the project."""
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional

# Set consistent plotting style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 12

def plot_time_series(t: np.ndarray, x: np.ndarray, labels: Optional[List[str]] = None, title: str = "Time Series"):
    """Plot time series of displacements or other variables."""
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
    """Plot phase space (x vs v)."""
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
    """Plot the mode shapes. modes should be a 2D array where columns are eigenvectors."""
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
    """Plot dispersion relation ? vs k."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(k, omega, 'b-', lw=2)
    ax.set_xlabel("Wavevector (k)")
    ax.set_ylabel("Angular Frequency (?)")
    ax.set_title(title)
    plt.tight_layout()
    return fig, ax
