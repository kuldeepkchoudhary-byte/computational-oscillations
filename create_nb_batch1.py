import json
import os

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
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

# 00_foundation/shm.ipynb
write_notebook(
    "00_foundation/shm.ipynb",
    "Simple Harmonic Motion & Energy Conservation",
    "## Theory\nEquation of motion: \ddot{x} = -kx$\nEnergy:  = \\frac{1}{2}mv^2 + \\frac{1}{2}kx^2$",
    '''import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from coupled_oscillators.plotting import plot_time_series

def shm_rhs(t, y, k, m):
    x, v = y
    return [v, -k/m * x]

sol = solve_ivp(shm_rhs, [0, 10], [1.0, 0.0], args=(1.0, 1.0), t_eval=np.linspace(0, 10, 200))
E = 0.5 * 1.0 * sol.y[1]**2 + 0.5 * 1.0 * sol.y[0]**2

fig, ax = plot_time_series(sol.t, sol.y[0], labels=["Position"], title="SHM Position")
plt.show()

fig2, ax2 = plot_time_series(sol.t, E, labels=["Total Energy"], title="Energy Conservation")
plt.show()
'''
)

# 01_linear_chains
write_notebook(
    "01_linear_chains/two_mass_1_spring.ipynb",
    "Two Masses, One Spring",
    "## Theory\nFree boundary conditions. Normal modes: center of mass translation and relative oscillation.",
    '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem, normalize_modes
from coupled_oscillators.plotting import plot_mode_shapes

K = build_k_matrix(2, boundary="free")
evals, evecs = solve_eigensystem(K)
evecs = normalize_modes(evecs)

print("Eigenfrequencies:", np.sqrt(np.abs(evals)))
fig, ax = plot_mode_shapes(evecs, title="Modes of 2-Mass 1-Spring System")
plt.show()
'''
)

write_notebook(
    "01_linear_chains/two_mass_3_spring.ipynb",
    "Two Masses, Three Springs",
    "## Theory\nFixed boundary conditions. Both ends attached to walls.",
    '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem
from coupled_oscillators.plotting import plot_mode_shapes

K = build_k_matrix(2, boundary="fixed")
evals, evecs = solve_eigensystem(K)

print("Eigenfrequencies:", np.sqrt(np.abs(evals)))
fig, ax = plot_mode_shapes(evecs, title="Modes of 2-Mass 3-Spring System")
plt.show()
'''
)

write_notebook(
    "01_linear_chains/three_mass_4_spring.ipynb",
    "Three Masses, Four Springs",
    "## Theory\nFixed boundaries with 3 masses.",
    '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem
from coupled_oscillators.plotting import plot_mode_shapes

K = build_k_matrix(3, boundary="fixed")
evals, evecs = solve_eigensystem(K)

print("Eigenfrequencies:", np.sqrt(np.abs(evals)))
fig, ax = plot_mode_shapes(evecs, title="Modes of 3-Mass 4-Spring System")
plt.show()
'''
)
