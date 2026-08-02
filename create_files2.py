# -*- coding: utf-8 -*-
import os

files = {}

files["src/coupled_oscillators/linear_chain.py"] = '''\
"\""Finite linear chains mechanics."\""
import numpy as np
from typing import Tuple

def build_k_matrix(N: int, k: float = 1.0, boundary: str = "fixed") -> np.ndarray:
    "\""Construct stiffness (K) matrix for N masses."\""
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
    "\""Construct mass matrix for N masses."\""
    return np.eye(N) * m

def solve_eigensystem(K: np.ndarray, M: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
    "\""Generalized eigenproblem Kx = omega^2 Mx."\""
    if M is None:
        M = np.eye(K.shape[0])
    from scipy.linalg import eigh
    evals, evecs = eigh(K, M)
    return sort_modes(evals, evecs)

def analytical_omegas_fixed(N: int, k: float = 1.0, m: float = 1.0) -> np.ndarray:
    "\""Compute closed-form normal-mode frequencies for fixed-end chain."\""
    j = np.arange(1, N + 1)
    return 2 * np.sqrt(k / m) * np.sin(j * np.pi / (2 * (N + 1)))

def normalize_modes(evecs: np.ndarray) -> np.ndarray:
    "\""Ensure eigenvectors are orthonormal (unit length)."\""
    norms = np.linalg.norm(evecs, axis=0)
    return evecs / norms

def sort_modes(evals: np.ndarray, evecs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    "\""Sort eigenvalues & eigenvectors in ascending omega."\""
    idx = np.argsort(evals)
    return evals[idx], evecs[:, idx]
'''

files["src/coupled_oscillators/modal_analysis.py"] = '''\
"\""Modal projection and reconstruction."\""
import numpy as np

def project_initial_condition(x0: np.ndarray, modes: np.ndarray) -> np.ndarray:
    "\""Compute modal coefficients a_j = V_j dot x0."\""
    return modes.T @ x0

def reconstruct_state(modes: np.ndarray, coeffs: np.ndarray, omega: np.ndarray, t: float) -> np.ndarray:
    "\""Compute displacement x(t) = Sum a_j cos(omega_j t) V_j."\""
    time_evolution = coeffs * np.cos(omega * t)
    return modes @ time_evolution

def mode_overlap_matrix(modes: np.ndarray) -> np.ndarray:
    "\""Compute V^T V."\""
    return modes.T @ modes

def check_orthogonality(modes: np.ndarray, tol: float = 1e-10) -> bool:
    "\""Verify V^T V is identity to tolerance."\""
    overlap = mode_overlap_matrix(modes)
    I = np.eye(modes.shape[1])
    return np.allclose(overlap, I, atol=tol)

def check_completeness(modes: np.ndarray, tol: float = 1e-10) -> bool:
    "\""Verify V V^T is identity to tolerance."\""
    completeness_mat = modes @ modes.T
    I = np.eye(modes.shape[0])
    return np.allclose(completeness_mat, I, atol=tol)

def modal_energy(x: np.ndarray, v: np.ndarray, modes: np.ndarray, omega: np.ndarray, m: float = 1.0) -> np.ndarray:
    "\""Compute energy in each mode given displacements and velocities."\""
    q = modes.T @ x
    q_dot = modes.T @ v
    return 0.5 * m * (q_dot**2 + (omega**2) * (q**2))
'''

files["src/coupled_oscillators/wave_analysis.py"] = '''\
"\""Infinite-chain and wave packets."\""
import numpy as np

def dispersion_relation(k: np.ndarray, a: float, k_spring: float, m: float) -> np.ndarray:
    "\""omega(k) = 2*sqrt(k_spring/m)*abs(sin(ka/2))."\""
    return 2 * np.sqrt(k_spring / m) * np.abs(np.sin(k * a / 2))

def phase_velocity(omega: np.ndarray, k: np.ndarray) -> np.ndarray:
    "\""omega/k for k>0."\""
    v_p = np.zeros_like(omega)
    mask = k != 0
    v_p[mask] = omega[mask] / k[mask]
    return v_p

def group_velocity(omega_k: np.ndarray, k_grid: np.ndarray) -> np.ndarray:
    "\""Compute d_omega/d_k using finite differences."\""
    return np.gradient(omega_k, k_grid)

def build_wave_packet(k0: float, sigma_k: float, x_grid: np.ndarray) -> np.ndarray:
    "\""Construct initial displacement as a Gaussian-weighted superposition around k0."\""
    envelope = np.exp(- (x_grid - np.mean(x_grid))**2 / (2 * (1/sigma_k)**2))
    return envelope * np.cos(k0 * x_grid)

def fft_mode_spectrum(signal: np.ndarray, dt: float) -> tuple:
    "\""Compute frequency spectrum of a time-series signal."\""
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=dt)
    spectrum = np.abs(np.fft.rfft(signal))
    return freqs, spectrum
'''

files["src/coupled_oscillators/lc_chain.py"] = '''\
"\""Electrical analogues (LC oscillators)."\""
import numpy as np

def build_lc_matrix(N: int, L: float = 1.0, C: float = 1.0, Cc: float = 0.0) -> np.ndarray:
    "\""Stiffness matrix for LC ladder with coupling Cc."\""
    K = np.zeros((N, N))
    for i in range(N):
        K[i, i] = 1.0 / (L * C) + 2.0 * Cc / (L * C)
        if i > 0:
            K[i, i-1] = -Cc / (L * C)
        if i < N - 1:
            K[i, i+1] = -Cc / (L * C)
    return K

def single_lc_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    "\""ODE for single LC oscillator (charge/flux). y = [q, i]"\""
    q, i = y
    L = params.get("L", 1.0)
    C = params.get("C", 1.0)
    return np.array([i, -q / (L * C)])

def coupled_lc_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    "\""ODEs for two coupled LC circuits."\""
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
    "\""Analytical omega(k) for infinite LC line."\""
    return np.sqrt(1/(L*C) + (4*Cc/(L*C)) * np.sin(k/2)**2)

def lc_cutoff_frequency(L: float, C: float) -> float:
    "\""omega_cutoff = 1/sqrt(LC)."\""
    return 1.0 / np.sqrt(L * C)

def compare_lc_mechanical(omega_lc: np.ndarray, omega_mech: np.ndarray) -> float:
    "\""Utility to compare LC and mass-spring spectra (returns max difference)."\""
    return np.max(np.abs(omega_lc - omega_mech))
'''

files["src/coupled_oscillators/animation.py"] = '''\
"\""Create animations (GIFs/MP4) for the project."\""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_chain(x_history: np.ndarray, node_positions: np.ndarray, dt: float, filename: str):
    "\""Produce an animation of moving masses."\""
    fig, ax = plt.subplots(figsize=(8, 3))
    line, = ax.plot(node_positions, x_history[0], 'o-')
    ax.set_ylim(np.min(x_history)*1.2, np.max(x_history)*1.2)
    ax.set_title("Chain Animation")
    
    def update(frame):
        line.set_ydata(x_history[frame])
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(x_history), blit=True, interval=dt*1000)
    ani.save(filename, writer='pillow')
    plt.close(fig)

def animate_mode(x_mode: np.ndarray, node_positions: np.ndarray, filename: str, frames: int=40):
    "\""Animate one normal mode."\""
    t_vals = np.linspace(0, 2*np.pi, frames)
    history = np.array([x_mode * np.cos(t) for t in t_vals])
    animate_chain(history, node_positions, 2.0/frames, filename)

def animate_spin_precession(spin_history: np.ndarray, cell_grid: np.ndarray, dt: float, filename: str):
    "\""Animate spin precession."\""
    pass
'''

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
