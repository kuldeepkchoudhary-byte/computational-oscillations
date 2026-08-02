import numpy as np
from coupled_oscillators.wave_analysis import dispersion_relation

def test_dispersion_relation():
    k = np.array([0.0, np.pi])
    omega = dispersion_relation(k, a=1.0, k_spring=1.0, m=1.0)
    assert np.isclose(omega[0], 0.0)
    assert np.isclose(omega[1], 2.0)
