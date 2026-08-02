"""Nonlinear oscillator and chain dynamics."""
import numpy as np

def duffing_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    """RHS of Duffing oscillator ODE, y=[x,v]."""
    x, v = y
    m = params.get("m", 1.0)
    c = params.get("c", 0.0)
    k = params.get("k", 1.0)
    alpha = params.get("alpha", 0.0)
    beta = params.get("beta", 0.0)
    
    dv_dt = -(c * v + k * x + alpha * x**2 + beta * x**3) / m
    return np.array([v, dv_dt])

def fpu_rhs(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    """RHS for FPU chain."""
    N = len(y) // 2
    x = y[:N]
    v = y[N:]
    
    m = params.get("m", 1.0)
    k = params.get("k", 1.0)
    alpha = params.get("alpha", 0.0)
    beta = params.get("beta", 0.0)
    
    # Pad x with zeros for fixed boundaries
    x_pad = np.pad(x, (1, 1), mode='constant')
    
    # Delta x_i = x_{i} - x_{i-1}
    # For forces, we need F_i = k(x_{i+1} - x_i) - k(x_i - x_{i-1}) + ...
    # Force from right spring minus force from left spring
    
    dx_right = x_pad[2:] - x_pad[1:-1]
    dx_left = x_pad[1:-1] - x_pad[:-2]
    
    F_linear = k * (dx_right - dx_left)
    F_alpha = alpha * (dx_right**2 - dx_left**2)
    F_beta = beta * (dx_right**3 - dx_left**3)
    
    a = (F_linear + F_alpha + F_beta) / m
    return np.concatenate([v, a])

def rk4_step(f, t: float, y: np.ndarray, dt: float, params: dict) -> np.ndarray:
    """One step of 4th-order Runge-Kutta."""
    k1 = f(t, y, params)
    k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1, params)
    k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2, params)
    k4 = f(t + dt, y + dt * k3, params)
    return y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

def integrate_system(rhs, y0: np.ndarray, t_grid: np.ndarray, params: dict) -> np.ndarray:
    """High-level integrator using custom RK4."""
    y_history = np.zeros((len(t_grid), len(y0)))
    y_history[0] = y0
    y = y0.copy()
    
    for i in range(1, len(t_grid)):
        dt = t_grid[i] - t_grid[i-1]
        y = rk4_step(rhs, t_grid[i-1], y, dt, params)
        y_history[i] = y
        
    return y_history

def compute_poincare_section(solution: np.ndarray, period: int, phases: int) -> np.ndarray:
    """Sample state at multiples of a base period."""
    # Basic implementation
    return solution[::period]
