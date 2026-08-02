# Coupled Oscillators and Magnonics - Project Summary

## Executive Summary
This repository contains a comprehensive suite of numerical simulations and Jupyter notebooks demonstrating the physics of coupled oscillators, extending from basic linear chains to nonlinear lattices and advanced spin-wave magnonics.

## Modules Implemented
- **Linear Dynamics**: shm.ipynb, linear chains, orthogonality, and completeness using normal mode analysis.
- **Wave Physics & Phonons**: Dispersion relations, wave packets, quantum oscillator heat capacities.
- **Nonlinear Dynamics (Phase A)**: Duffing oscillators, Fermi-Pasta-Ulam (FPU) chains, showing energy recurrence and solitary waves.
- **Spin Dynamics & Magnonics (Phase B)**: Solutions to the Landau-Lifshitz-Gilbert (LLG) equation, domain walls, and magnonic crystals with bandgaps.

## Package Architecture
The src/coupled_oscillators package provides all heavy-lifting routines:
- linear_chain.py: Eigensolvers for mass-spring matrices.
- 
onlinear.py: RK4 integrators for Duffing and FPU chains.
- spin_dynamics.py: LLG integrations with exchange and anisotropy fields.
- magnonics.py: Spatial profiles for magnonic crystals and domain walls.

All notebooks are designed to be reproducible, strictly separating the numerical engines (in src) from the exploratory interfaces (in notebooks).

## Testing
Unit tests cover all core functions in the 	ests/ directory and pass continuously.
