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
        [1.0, 1.1, 1.2, 1.31, 1.41],
        [1.4, 1.3, 1.25, 1.41, 1.51]
    ])
    g = hybrid_mode_fit(freqs, np.arange(5))
    # gap at index 2 is 1.25 - 1.2 = 0.05
    assert np.isclose(g, 0.025)
