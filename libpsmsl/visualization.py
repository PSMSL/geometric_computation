"""
PSMSL Visualization: Plotting and Animation Utilities
======================================================
Tools for visualizing tetrahedra, lattices, and phase transitions.

Copyright 2025 Nathanael Joseph Bocker and contributors
Licensed under the Apache License, Version 2.0
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Optional
from .psmsl_core import Tetrahedron, TriadicState
from .lattice import GeometricLattice


def plot_tetrahedron_3d(tetra: Tetrahedron, ax: Optional[plt.Axes] = None, **kwargs):
    """
    Plot a single tetrahedron in 3D space.
    
    Args:
        tetra: The tetrahedron to plot
        ax: Matplotlib 3D axes (creates new if None)
        **kwargs: Additional arguments passed to plot()
    
    Returns:
        The axes object
    """
    if ax is None:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
    
    # Define tetrahedron vertices in 3D
    # Using standard tetrahedron coordinates
    vertices = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ], dtype=float)
    
    # Scale by depth (φ-scaling)
    from .psmsl_core import PHI
    scale = PHI ** tetra.depth
    vertices *= scale
    
    # Draw edges
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3), (2, 3)
    ]
    
    for edge in edges:
        points = vertices[list(edge)]
        ax.plot3D(*points.T, 'b-', **kwargs)
    
    # Draw vertices
    ax.scatter3D(*vertices.T, c='r', s=50, **kwargs)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Tetrahedron (depth={tetra.depth})')
    
    return ax


def plot_triadic_properties(states: List[TriadicState], figsize=(12, 8)):
    """
    Plot the evolution of triadic properties over time.
    
    Args:
        states: List of TriadicState objects (time series)
        figsize: Figure size tuple
    
    Returns:
        The figure object
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    T_vals = [s.T_persistence for s in states]
    M_vals = [s.M_curvature for s in states]
    rho_vals = [s.rho_E_flux for s in states]
    sigma_vals = [s.sigma_entropy for s in states]
    
    time = np.arange(len(states))
    
    axes[0, 0].plot(time, T_vals, 'b-', linewidth=2)
    axes[0, 0].set_ylabel('T (Persistence)', fontsize=12)
    axes[0, 0].set_title('Time', fontsize=13, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(time, M_vals, 'r-', linewidth=2)
    axes[0, 1].set_ylabel('M (Curvature)', fontsize=12)
    axes[0, 1].set_title('Mass', fontsize=13, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].plot(time, rho_vals, 'g-', linewidth=2)
    axes[1, 0].set_ylabel('ρ_E (Flux)', fontsize=12)
    axes[1, 0].set_xlabel('Step', fontsize=12)
    axes[1, 0].set_title('Energy Density', fontsize=13, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(time, sigma_vals, 'm-', linewidth=2)
    axes[1, 1].set_ylabel('σ (Entropy)', fontsize=12)
    axes[1, 1].set_xlabel('Step', fontsize=12)
    axes[1, 1].set_title('Mirror Drift', fontsize=13, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_lattice_network(lattice: GeometricLattice, figsize=(10, 10)):
    """
    Plot the lattice as a network graph showing connectivity.
    
    Args:
        lattice: The GeometricLattice to visualize
        figsize: Figure size tuple
    
    Returns:
        The figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create a simple 2D layout for visualization
    n = len(lattice)
    if n == 0:
        ax.text(0.5, 0.5, 'Empty Lattice', ha='center', va='center', fontsize=16)
        return fig
    
    # Arrange nodes in a circle
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    positions = {tid: (np.cos(angle), np.sin(angle)) for tid, angle in zip(lattice.tetrahedra.keys(), angles)}
    
    # Draw edges (connections)
    for tid, connections in lattice.connectivity.items():
        x1, y1 = positions[tid]
        for face_id, neighbor_id in connections.items():
            if neighbor_id is not None and neighbor_id > tid:  # Draw each edge once
                x2, y2 = positions[neighbor_id]
                ax.plot([x1, x2], [y1, y2], 'b-', alpha=0.3, linewidth=1)
    
    # Draw nodes
    for tid, (x, y) in positions.items():
        entropy = lattice.states[tid].sigma_entropy
        # Color by entropy level
        color = plt.cm.viridis(entropy / (max(s.sigma_entropy for s in lattice.states.values()) + 1e-10))
        ax.scatter(x, y, c=[color], s=300, edgecolors='black', linewidths=2)
        ax.text(x, y, str(tid), ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Lattice Network (n={n})', fontsize=14, fontweight='bold')
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=max(s.sigma_entropy for s in lattice.states.values())))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Entropy (σ)', fontsize=12)
    
    return fig


def plot_phase_space(states: List[TriadicState], figsize=(10, 8)):
    """
    Plot the trajectory in T-M-ρ_E phase space.
    
    Args:
        states: List of TriadicState objects (time series)
        figsize: Figure size tuple
    
    Returns:
        The figure object
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    T_vals = np.array([s.T_persistence for s in states])
    M_vals = np.array([s.M_curvature for s in states])
    rho_vals = np.array([s.rho_E_flux for s in states])
    
    # Plot trajectory
    ax.plot3D(T_vals, M_vals, rho_vals, 'b-', linewidth=2, alpha=0.7)
    
    # Mark start and end
    ax.scatter3D([T_vals[0]], [M_vals[0]], [rho_vals[0]], c='g', s=100, label='Start', zorder=5)
    ax.scatter3D([T_vals[-1]], [M_vals[-1]], [rho_vals[-1]], c='r', s=100, label='End', zorder=5)
    
    ax.set_xlabel('T (Persistence)', fontsize=12)
    ax.set_ylabel('M (Curvature)', fontsize=12)
    ax.set_zlabel('ρ_E (Flux)', fontsize=12)
    ax.set_title('Phase Space Trajectory', fontsize=14, fontweight='bold')
    ax.legend()
    
    return fig
