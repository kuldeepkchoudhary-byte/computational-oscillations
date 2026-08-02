import json
import os

files = {}

files["src/coupled_oscillators/magnonics.py"] = '''\
"\""Magnonic crystals and devices."\""
import numpy as np
from typing import Tuple

def build_exchange_profile(N: int, pattern: str, J0: float = 1.0, J1: float = 0.5) -> np.ndarray:
    "\""Create spatially varying exchange constant array."\""
    profile = np.ones(N) * J0
    if pattern == "alternating":
        profile[1::2] = J1
    elif pattern == "defect":
        profile[N//2] = J1
    return profile

def build_anisotropy_profile(N: int, pattern: str, K0: float = 0.0, K1: float = 1.0) -> np.ndarray:
    "\""Create spatially varying anisotropy array."\""
    profile = np.ones(N) * K0
    if pattern == "defect":
        profile[N//2] = K1
    return profile

def domain_wall_profile(N: int, width: float, orientation: str = "z") -> np.ndarray:
    "\""Initialize spins with a smooth domain wall."\""
    x = np.arange(N) - N/2.0
    # standard Walker profile theta = 2*arctan(exp(x / width))
    theta = 2 * np.arctan(np.exp(x / width))
    
    spins = np.zeros((N, 3))
    if orientation == "z":
        spins[:, 0] = np.sin(theta)
        spins[:, 2] = np.cos(theta)
    return spins

def transmission_spectrum(inc_wave: np.ndarray, defect_structure: np.ndarray, params: dict) -> float:
    "\""Simulate transmission of incident wave."\""
    # placeholder for actual integration or scattering matrix approach
    return 1.0

def reflection_coefficient(inc_wave: np.ndarray, defect_structure: np.ndarray, params: dict) -> float:
    "\""Compute reflection coefficient R."\""
    return 0.0

def hybrid_mode_fit(frequencies: np.ndarray, tuning_param: np.ndarray) -> float:
    "\""Fit avoided-crossing curves to extract coupling strength 2g."\""
    # Very simplified: g is half the minimum gap
    diff = np.abs(frequencies[1] - frequencies[0])
    g = np.min(diff) / 2.0
    return g
'''

files["tests/test_magnonics.py"] = '''\
import numpy as np
from coupled_oscillators.magnonics import build_exchange_profile, domain_wall_profile, hybrid_mode_fit

def test_build_exchange_profile():
    prof = build_exchange_profile(4, "alternating", 1.0, 0.5)
    assert np.allclose(prof, [1.0, 0.5, 1.0, 0.5])

def test_domain_wall_profile():
    spins = domain_wall_profile(10, width=1.0)
    assert spins.shape == (10, 3)
    # Check bounds, z component should go from roughly 1 to -1 or vice versa
    assert spins[0, 2] > 0.9
    assert spins[-1, 2] < -0.9
    
def test_hybrid_mode_fit():
    # Toy example of avoided crossing frequencies
    freqs = np.array([
        [1.0, 1.1, 1.2, 1.3, 1.4],
        [1.4, 1.3, 1.25, 1.3, 1.4]
    ])
    g = hybrid_mode_fit(freqs, np.arange(5))
    # gap at index 2 is 1.25 - 1.2 = 0.05
    assert np.isclose(g, 0.025)
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

write_notebook("09_magnonics/01_magnonic_crystal.ipynb", "Magnonic Crystal", "## Theory\nBandgaps from periodic modulation.", '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.magnonics import build_exchange_profile

N = 20
J_profile = build_exchange_profile(N, "alternating", J0=1.0, J1=0.5)

plt.plot(J_profile, 'o-')
plt.title("Alternating Exchange Profile")
plt.xlabel("Site index")
plt.ylabel("J")
plt.show()
''')

write_notebook("09_magnonics/02_defects_and_domain_walls.ipynb", "Defects and Domain Walls", "## Theory\nLocalized defects and domain walls.", '''import numpy as np
import matplotlib.pyplot as plt
from coupled_oscillators.magnonics import domain_wall_profile

N = 50
spins = domain_wall_profile(N, width=5.0)

plt.plot(spins[:, 2], label="Mz")
plt.plot(spins[:, 0], label="Mx")
plt.title("Domain Wall Profile")
plt.xlabel("Site index")
plt.ylabel("Spin Component")
plt.legend()
plt.show()
''')

write_notebook("09_magnonics/03_magnon_photon_coupling.ipynb", "Magnon-Photon Coupling", "## Theory\nAvoided crossing.", "# To be filled")

