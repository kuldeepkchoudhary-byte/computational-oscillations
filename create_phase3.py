import json
import os

files = {}

files["src/coupled_oscillators/nonlinear.py"] = '''\
"\""Nonlinear oscillator and chain dynamics."\""
import numpy as np

def duffing_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    "\""RHS of Duffing oscillator ODE, y=[x,v]."\""
    x, v = y
    m = params.get("m", 1.0)
    c = params.get("c", 0.0)
    k = params.get("k", 1.0)
    alpha = params.get("alpha", 0.0)
    beta = params.get("beta", 0.0)
    
    dv_dt = -(c * v + k * x + alpha * x**2 + beta * x**3) / m
    return np.array([v, dv_dt])

def fpu_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    "\""RHS for FPU chain."\""
    N = len(y) // 2
    x = y[:N]
    v = y[N:]
    
    m = params.get("m", 1.0)
    k = params.get("k", 1.0)
    alpha = params.get("alpha", 0.0)
    beta = params.get("beta", 0.0)
    
    # Pad x with zeros for fixed boundaries
    x_pad = np.pad(x, (1, 1), mode='constant')
    
    # Delta x_i = x_{i} - x_{i-1}
    # For forces, we need F_i = k(x_{i+1} - x_i) - k(x_i - x_{i-1}) + ...
    # Force from right spring minus force from left spring
    
    dx_right = x_pad[2:] - x_pad[1:-1]
    dx_left = x_pad[1:-1] - x_pad[:-2]
    
    F_linear = k * (dx_right - dx_left)
    F_alpha = alpha * (dx_right**2 - dx_left**2)
    F_beta = beta * (dx_right**3 - dx_left**3)
    
    a = (F_linear + F_alpha + F_beta) / m
    return np.concatenate([v, a])

def rk4_step(f, t: float, y: np.ndarray, dt: float, params: dict) -> np.ndarray:
    "\""One step of 4th-order Runge-Kutta."\""
    k1 = f(t, y, params)
    k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1, params)
    k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2, params)
    k4 = f(t + dt, y + dt * k3, params)
    return y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

def integrate_system(rhs, y0: np.ndarray, t_grid: np.ndarray, params: dict) -> np.ndarray:
    "\""High-level integrator using custom RK4."\""
    y_history = np.zeros((len(t_grid), len(y0)))
    y_history[0] = y0
    y = y0.copy()
    
    for i in range(1, len(t_grid)):
        dt = t_grid[i] - t_grid[i-1]
        y = rk4_step(rhs, t_grid[i-1], y, dt, params)
        y_history[i] = y
        
    return y_history

def compute_poincare_section(solution: np.ndarray, period: int, phases: int) -> np.ndarray:
    "\""Sample state at multiples of a base period."\""
    # Basic implementation
    return solution[::period]
'''

files["tests/test_nonlinear.py"] = '''\
import numpy as np
from coupled_oscillators.nonlinear import duffing_rhs, fpu_rhs, rk4_step

def test_duffing_rhs():
    y = np.array([1.0, 0.0])
    params = {"m": 1.0, "k": 1.0, "beta": 1.0}
    dy = duffing_rhs(0.0, y, params)
    assert np.allclose(dy, [0.0, -2.0]) # -(1*1 + 1*1^3) = -2

def test_fpu_rhs():
    y = np.array([1.0, 0.0, 0.0, 0.0]) # N=2, x=[1,0], v=[0,0]
    params = {"m": 1.0, "k": 1.0, "beta": 0.0}
    dy = fpu_rhs(0.0, y, params)
    # x=[1, 0], x_pad=[0, 1, 0, 0]
    # dx_right = [0-1, 0-0] = [-1, 0]
    # dx_left = [1-0, 0-1] = [1, -1]
    # F_linear = dx_right - dx_left = [-2, 1]
    assert np.allclose(dy, [0.0, 0.0, -2.0, 1.0])
'''

def write_notebook(path, title, theory_md, code_content):
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n",
                    "\n",
                    theory_md
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_content.splitlines(True)
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

write_notebook("07_nonlinear/01_duffing_oscillator.ipynb", "Duffing Oscillator", "## Theory\nEquation: \ddot x + c\dot x + kx + \\alpha x^2 + \\beta x^3 = 0$", '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.nonlinear import duffing_rhs, integrate_system
from coupled_oscillators.plotting import plot_time_series, plot_phase_space

params = {"m": 1.0, "c": 0.0, "k": 1.0, "alpha": 0.0, "beta": 1.0}
t_grid = np.linspace(0, 50, 1000)
y0 = np.array([2.0, 0.0])

sol = integrate_system(duffing_rhs, y0, t_grid, params)
x, v = sol[:, 0], sol[:, 1]

fig1, ax1 = plot_time_series(t_grid, x, labels=["Position"], title="Duffing Hardening Spring")
plt.show()

fig2, ax2 = plot_phase_space(x, v, title="Duffing Phase Space")
plt.show()
''')

write_notebook("07_nonlinear/02_fpu_chain.ipynb", "Fermi-Pasta-Ulam Chain", "## Theory\nNonlinear nearest-neighbor force.", '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.nonlinear import fpu_rhs, integrate_system
from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem, normalize_modes
from coupled_oscillators.modal_analysis import modal_energy

N = 16
K = build_k_matrix(N, boundary="fixed")
evals, evecs = solve_eigensystem(K)
evecs = normalize_modes(evecs)
omegas = np.sqrt(np.abs(evals))

y0 = np.zeros(2*N)
y0[:N] = evecs[:, 0] * 2.0 # seed first mode

params = {"m": 1.0, "k": 1.0, "alpha": 0.0, "beta": 0.1}
t_grid = np.linspace(0, 1000, 20000)
sol = integrate_system(fpu_rhs, y0, t_grid, params)

mode_energies = np.zeros((len(t_grid), N))
for i in range(len(t_grid)):
    mode_energies[i] = modal_energy(sol[i, :N], sol[i, N:], evecs, omegas)

plt.figure(figsize=(10,6))
for i in range(4):
    plt.plot(t_grid, mode_energies[:, i], label=f"Mode {i+1}")
plt.title("FPU Recurrence (Energy in first few modes)")
plt.xlabel("Time")
plt.ylabel("Energy")
plt.legend()
plt.show()
''')

write_notebook("07_nonlinear/03_solitons_breathers.ipynb", "Solitons & Breathers", "## Theory\nLocalized nonlinear phenomena.", "# To be filled")
write_notebook("07_nonlinear/04_nonlinear_analysis_tools.ipynb", "Nonlinear Analysis Tools", "## Theory\nFourier analysis, convergence, phase-space.", "# To be filled")
