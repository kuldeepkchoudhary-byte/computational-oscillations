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
