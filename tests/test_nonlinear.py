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
