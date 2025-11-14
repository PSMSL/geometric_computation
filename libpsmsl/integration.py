"""
PSMSL Integration: NumPy and Pandas Utilities
==============================================
Tools for converting between PSMSL objects and standard data structures.

Copyright 2025 Nathanael Joseph Bocker and contributors
Licensed under the Apache License, Version 2.0
"""

import numpy as np
from typing import List, Dict
from .psmsl_core import Tetrahedron, TriadicState
from .lattice import GeometricLattice

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def states_to_array(states: List[TriadicState]) -> np.ndarray:
    """
    Convert a list of TriadicState objects to a NumPy array.
    
    Args:
        states: List of TriadicState objects
    
    Returns:
        NumPy array of shape (n_states, 4) with columns [T, M, ρ_E, σ]
    """
    return np.array([
        [s.T_persistence, s.M_curvature, s.rho_E_flux, s.sigma_entropy]
        for s in states
    ])


def lattice_to_array(lattice: GeometricLattice) -> np.ndarray:
    """
    Convert a GeometricLattice to a NumPy array.
    
    Args:
        lattice: The GeometricLattice to convert
    
    Returns:
        NumPy array of shape (n_tetrahedra, 4) with columns [T, M, ρ_E, σ]
    """
    states = [lattice.states[tid] for tid in sorted(lattice.tetrahedra.keys())]
    return states_to_array(states)


def states_to_dataframe(states: List[TriadicState]) -> 'pd.DataFrame':
    """
    Convert a list of TriadicState objects to a Pandas DataFrame.
    
    Args:
        states: List of TriadicState objects
    
    Returns:
        Pandas DataFrame with columns [T, M, rho_E, sigma, depth]
    
    Raises:
        ImportError: If pandas is not installed
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("Pandas is required for this function. Install with: pip install pandas")
    
    data = {
        'T': [s.T_persistence for s in states],
        'M': [s.M_curvature for s in states],
        'rho_E': [s.rho_E_flux for s in states],
        'sigma': [s.sigma_entropy for s in states],
        'depth': [s.tetrahedron.depth for s in states],
    }
    
    return pd.DataFrame(data)


def lattice_to_dataframe(lattice: GeometricLattice) -> 'pd.DataFrame':
    """
    Convert a GeometricLattice to a Pandas DataFrame.
    
    Args:
        lattice: The GeometricLattice to convert
    
    Returns:
        Pandas DataFrame with columns [tetra_id, T, M, rho_E, sigma, depth, n_neighbors]
    
    Raises:
        ImportError: If pandas is not installed
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("Pandas is required for this function. Install with: pip install pandas")
    
    data = {
        'tetra_id': [],
        'T': [],
        'M': [],
        'rho_E': [],
        'sigma': [],
        'depth': [],
        'n_neighbors': [],
    }
    
    for tid in sorted(lattice.tetrahedra.keys()):
        state = lattice.states[tid]
        neighbors = lattice.get_neighbors(tid)
        n_neighbors = sum(1 for n in neighbors if n is not None)
        
        data['tetra_id'].append(tid)
        data['T'].append(state.T_persistence)
        data['M'].append(state.M_curvature)
        data['rho_E'].append(state.rho_E_flux)
        data['sigma'].append(state.sigma_entropy)
        data['depth'].append(state.tetrahedron.depth)
        data['n_neighbors'].append(n_neighbors)
    
    return pd.DataFrame(data)


def batch_project_forward(states: List[TriadicState]) -> List[TriadicState]:
    """
    Project a batch of states forward in parallel (vectorized where possible).
    
    Args:
        states: List of TriadicState objects
    
    Returns:
        List of projected TriadicState objects
    """
    return [state.project_forward() for state in states]


def compute_statistics(states: List[TriadicState]) -> Dict[str, Dict[str, float]]:
    """
    Compute statistical measures for a collection of states.
    
    Args:
        states: List of TriadicState objects
    
    Returns:
        Dictionary with statistics for each property (T, M, ρ_E, σ)
    """
    arr = states_to_array(states)
    
    properties = ['T', 'M', 'rho_E', 'sigma']
    stats = {}
    
    for i, prop in enumerate(properties):
        stats[prop] = {
            'mean': float(np.mean(arr[:, i])),
            'std': float(np.std(arr[:, i])),
            'min': float(np.min(arr[:, i])),
            'max': float(np.max(arr[:, i])),
            'median': float(np.median(arr[:, i])),
        }
    
    return stats
