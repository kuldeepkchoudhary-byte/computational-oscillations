import os

files = {}

files["tests/test_linear_chain.py"] = '''\
import numpy as np
from coupled_oscillators.linear_chain import build_k_matrix, build_mass_matrix, solve_eigensystem, analytical_omegas_fixed

def test_build_k_matrix():
    K = build_k_matrix(2, k=1.0)
    assert K.shape == (2, 2)
    assert np.allclose(K, [[2, -1], [-1, 2]])

def test_solve_eigensystem():
    K = build_k_matrix(2, k=1.0)
    M = build_mass_matrix(2, m=1.0)
    evals, evecs = solve_eigensystem(K, M)
    omegas = np.sqrt(evals)
    expected = analytical_omegas_fixed(2, k=1.0, m=1.0)
    assert np.allclose(omegas, expected)
'''

files["tests/test_validation.py"] = '''\
import pytest
import numpy as np
from coupled_oscillators.validation import check_symmetric, check_positive_eigs, check_energy_conservation

def test_check_symmetric():
    K = np.array([[2, -1], [-1, 2]])
    assert check_symmetric(K)
    with pytest.raises(ValueError):
        check_symmetric(np.array([[2, 1], [-1, 2]]))

def test_check_positive_eigs():
    assert check_positive_eigs(np.array([0.1, 1.0, 2.0]))
    with pytest.raises(ValueError):
        check_positive_eigs(np.array([-0.1, 1.0]))

def test_check_energy_conservation():
    energies = np.array([1.0, 1.0, 1.000001])
    assert check_energy_conservation(energies)
    with pytest.raises(ValueError):
        check_energy_conservation(np.array([1.0, 1.0, 1.1]))
'''

files["tests/test_wave_analysis.py"] = '''\
import numpy as np
from coupled_oscillators.wave_analysis import dispersion_relation

def test_dispersion_relation():
    k = np.array([0.0, np.pi])
    omega = dispersion_relation(k, a=1.0, k_spring=1.0, m=1.0)
    assert np.isclose(omega[0], 0.0)
    assert np.isclose(omega[1], 2.0)
'''

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
