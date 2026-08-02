"""Landau-Lifshitz-Gilbert (LLG) spin dynamics."""
import numpy as np

def effective_field_exchange(spins: np.ndarray, params: dict) -> np.ndarray:
    """Compute exchange field from nearest-neighbor coupling J."""
    # spins shape: (N, 3)
    J = params.get("J", 1.0)
    H_exch = np.zeros_like(spins)
    # H_exch_i = J * (S_{i-1} + S_{i+1})
    if len(spins) > 1:
        H_exch[1:-1] = J * (spins[:-2] + spins[2:])
        H_exch[0] = J * spins[1]
        H_exch[-1] = J * spins[-2]
    return H_exch

def effective_field_anisotropy(spins: np.ndarray, params: dict) -> np.ndarray:
    """Compute uniaxial anisotropy field."""
    K_ani = params.get("K_ani", 0.0)
    # Easy axis assumed along z-axis (0, 0, 1)
    H_ani = np.zeros_like(spins)
    H_ani[:, 2] = 2 * K_ani * spins[:, 2]
    return H_ani

def effective_field_zeeman(params: dict, N: int) -> np.ndarray:
    """External field."""
    H_ext = params.get("H_ext", np.array([0.0, 0.0, 1.0]))
    return np.tile(H_ext, (N, 1))

def llg_rhs(t: float, M_flat: np.ndarray, params: dict) -> np.ndarray:
    """RHS of LLG equation."""
    N = len(M_flat) // 3
    spins = M_flat.reshape((N, 3))
    
    gamma = params.get("gamma", 1.0)
    alpha = params.get("alpha", 0.01)
    
    H_eff = (effective_field_exchange(spins, params) +
             effective_field_anisotropy(spins, params) +
             effective_field_zeeman(params, N))
             
    # Precession: -gamma * M x H_eff
    precession = -gamma * np.cross(spins, H_eff)
    
    # Gilbert damping: (alpha / |M|) * M x dM/dt
    # Implicit form for small alpha: dM/dt = (precession - alpha * gamma * M x (M x H_eff)) / (1 + alpha^2)
    damping = -alpha * gamma * np.cross(spins, np.cross(spins, H_eff))
    
    dM_dt = (precession + damping) / (1 + alpha**2)
    return dM_dt.flatten()

def normalize_spin(M_array: np.ndarray) -> np.ndarray:
    """Renormalize spin vectors to unit length."""
    N = len(M_array) // 3
    spins = M_array.reshape((N, 3))
    norms = np.linalg.norm(spins, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (spins / norms).flatten()

def integrate_llg(M0: np.ndarray, t_grid: np.ndarray, params: dict) -> np.ndarray:
    """Integrate LLG ODE system using scipy.solve_ivp."""
    from scipy.integrate import solve_ivp
    
    def rhs(t, y):
        # Optional: normalize periodically if needed, but doing it inside RHS breaks solver sometimes
        return llg_rhs(t, y, params)
        
    sol = solve_ivp(rhs, [t_grid[0], t_grid[-1]], M0, t_eval=t_grid, method='RK45')
    
    # Normalize output
    history = np.zeros_like(sol.y.T)
    for i in range(len(t_grid)):
        history[i] = normalize_spin(sol.y[:, i])
    return history

def spin_wave_fft(spin_time_series: np.ndarray, dt: float) -> tuple:
    """Compute magnon dispersion from space-time data via 2D FFT."""
    # spin_time_series shape: (time_steps, N_spins)
    fft2d = np.fft.fft2(spin_time_series)
    fft2d = np.fft.fftshift(fft2d)
    
    freqs = np.fft.fftshift(np.fft.fftfreq(spin_time_series.shape[0], d=dt))
    k_vals = np.fft.fftshift(np.fft.fftfreq(spin_time_series.shape[1], d=1.0))
    
    return k_vals, freqs, np.abs(fft2d)
