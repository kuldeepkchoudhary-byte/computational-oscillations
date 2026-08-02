"""Create animations (GIFs/MP4) for the project."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_chain(x_history: np.ndarray, node_positions: np.ndarray, dt: float, filename: str):
    """Produce an animation of moving masses."""
    fig, ax = plt.subplots(figsize=(8, 3))
    line, = ax.plot(node_positions, x_history[0], 'o-')
    ax.set_ylim(np.min(x_history)*1.2, np.max(x_history)*1.2)
    ax.set_title("Chain Animation")
    
    def update(frame):
        line.set_ydata(x_history[frame])
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(x_history), blit=True, interval=dt*1000)
    ani.save(filename, writer='pillow')
    plt.close(fig)

def animate_mode(x_mode: np.ndarray, node_positions: np.ndarray, filename: str, frames: int=40):
    """Animate one normal mode."""
    t_vals = np.linspace(0, 2*np.pi, frames)
    history = np.array([x_mode * np.cos(t) for t in t_vals])
    animate_chain(history, node_positions, 2.0/frames, filename)

def animate_spin_precession(spin_history: np.ndarray, cell_grid: np.ndarray, dt: float, filename: str):
    """Animate spin precession."""
    pass
