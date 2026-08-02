import json

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

# 02_analysis_tools
write_notebook(
    "02_analysis_tools/general_N.ipynb",
    "General N-Mass System",
    "## Theory\nExtracting eigenvalues and modes for an arbitrary N.",
    '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem, analytical_omegas_fixed

N = 10
K = build_k_matrix(N, boundary="fixed")
evals, evecs = solve_eigensystem(K)
omegas = np.sqrt(np.abs(evals))
omegas_analytical = analytical_omegas_fixed(N)

plt.plot(range(1, N+1), omegas, 'o', label='Numerical')
plt.plot(range(1, N+1), omegas_analytical, 'x', label='Analytical')
plt.xlabel("Mode index")
plt.ylabel("Frequency")
plt.legend()
plt.show()
'''
)

write_notebook(
    "02_analysis_tools/orthogonality.ipynb",
    "Orthogonality of Modes",
    "## Theory\nChecking if ^T V = I$ for orthonormal eigenvectors.",
    '''from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem, normalize_modes
from coupled_oscillators.modal_analysis import check_orthogonality

K = build_k_matrix(5, boundary="fixed")
evals, evecs = solve_eigensystem(K)
evecs = normalize_modes(evecs)

is_ortho = check_orthogonality(evecs)
print(f"Modes are orthogonal: {is_ortho}")
'''
)

write_notebook(
    "02_analysis_tools/completeness.ipynb",
    "Completeness of Modes",
    "## Theory\nChecking if  V^T = I$.",
    '''from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem, normalize_modes
from coupled_oscillators.modal_analysis import check_completeness

K = build_k_matrix(5, boundary="fixed")
evals, evecs = solve_eigensystem(K)
evecs = normalize_modes(evecs)

is_complete = check_completeness(evecs)
print(f"Modes form a complete basis: {is_complete}")
'''
)

write_notebook(
    "02_analysis_tools/energy_decomposition.ipynb",
    "Energy Decomposition",
    "## Theory\nDecomposing total energy into modal contributions.",
    '''import numpy as np
from coupled_oscillators.linear_chain import build_k_matrix, solve_eigensystem, normalize_modes
from coupled_oscillators.modal_analysis import modal_energy

K = build_k_matrix(5, boundary="fixed")
evals, evecs = solve_eigensystem(K)
evecs = normalize_modes(evecs)
omegas = np.sqrt(np.abs(evals))

x = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
v = np.zeros(5)

E_modes = modal_energy(x, v, evecs, omegas)
print("Energy in each mode:", E_modes)
print("Total modal energy:", np.sum(E_modes))
'''
)

# 03_wave_physics
write_notebook("03_wave_physics/dispersion.ipynb", "Dispersion Relation", "## Theory\n?(k) for infinite chain", '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.wave_analysis import dispersion_relation
from coupled_oscillators.plotting import plot_dispersion

k_vals = np.linspace(-np.pi, np.pi, 100)
omegas = dispersion_relation(k_vals, a=1.0, k_spring=1.0, m=1.0)
fig, ax = plot_dispersion(k_vals, omegas, title="Phonon Dispersion Relation")
plt.show()
''')

write_notebook("03_wave_physics/continuum_limit.ipynb", "Continuum Limit", "## Theory\nSmall k limit.", "# To be filled")
write_notebook("03_wave_physics/wave_packets.ipynb", "Wave Packets", "## Theory\nSuperposition of plane waves.", "# To be filled")

# 04_lc_oscillators
write_notebook("04_lc_oscillators/single_lc.ipynb", "Single LC Circuit", "## Theory\nCharge and flux oscillation.", "# To be filled")
write_notebook("04_lc_oscillators/coupled_lc.ipynb", "Coupled LC Circuits", "## Theory\nTwo LC circuits.", "# To be filled")
write_notebook("04_lc_oscillators/lc_chain.ipynb", "LC Ladder Network", "## Theory\nChain of LC circuits.", "# To be filled")
write_notebook("04_lc_oscillators/lc_dispersion.ipynb", "LC Dispersion", "## Theory\nDispersion in LC line.", "# To be filled")

# 05_phonons
write_notebook("05_phonons/quantum_oscillator.ipynb", "Quantum Oscillator", "## Theory\nQuantized energies.", "# To be filled")
write_notebook("05_phonons/bose_statistics.ipynb", "Bose Statistics", "## Theory\nPhonon occupation.", "# To be filled")
write_notebook("05_phonons/heat_capacity.ipynb", "Heat Capacity", "## Theory\nEinstein/Debye models.", "# To be filled")

# 06_defects & 07_disorder
write_notebook("06_defects/single_defect.ipynb", "Single Defect", "## Theory\nLocalized impurity mode.", "# To be filled")
write_notebook("06_defects/localized_modes.ipynb", "Localized Modes", "## Theory\nDecay length.", "# To be filled")
write_notebook("06_defects/scattering.ipynb", "Scattering", "## Theory\nTransmission/reflection.", "# To be filled")
write_notebook("07_disorder/random_chains.ipynb", "Random Chains", "## Theory\nDisordered masses.", "# To be filled")
write_notebook("07_disorder/anderson_localization.ipynb", "Anderson Localization", "## Theory\nExponential localization.", "# To be filled")

