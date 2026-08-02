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
