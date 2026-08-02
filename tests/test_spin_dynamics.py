import numpy as np
from coupled_oscillators.spin_dynamics import effective_field_exchange, normalize_spin

def test_effective_field_exchange():
    spins = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    params = {"J": 1.0}
    H = effective_field_exchange(spins, params)
    assert np.allclose(H[1], [1, 0, 1])

def test_normalize_spin():
    M = np.array([2.0, 0.0, 0.0, 0.0, 3.0, 4.0])
    M_norm = normalize_spin(M)
    assert np.allclose(M_norm, [1.0, 0.0, 0.0, 0.0, 0.6, 0.8])
