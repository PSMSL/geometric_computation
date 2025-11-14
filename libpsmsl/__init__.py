"""
PSMSL: The Geometric Computational Engine
==========================================

Copyright 2025 Nathanael Joseph Bocker and contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__version__ = "0.1.0"
__author__ = "Nathanael Joseph Bocker and contributors"
__license__ = "Apache-2.0"

from .psmsl_core import (
    PHI,
    TensorFace,
    Tetrahedron,
    TriadicState,
    PhaseTransitionDetector,
    PhaseTransitionEngine,
    handle_imaginary_via_rotation,
)

from .lattice import GeometricLattice

from .visualization import (
    plot_tetrahedron_3d,
    plot_triadic_properties,
    plot_lattice_network,
    plot_phase_space,
)

from .integration import (
    states_to_array,
    lattice_to_array,
    states_to_dataframe,
    lattice_to_dataframe,
    batch_project_forward,
    compute_statistics,
)

__all__ = [
    # Core primitives
    "PHI",
    "TensorFace",
    "Tetrahedron",
    "TriadicState",
    "PhaseTransitionDetector",
    "PhaseTransitionEngine",
    "handle_imaginary_via_rotation",
    # Lattice management
    "GeometricLattice",
    # Visualization
    "plot_tetrahedron_3d",
    "plot_triadic_properties",
    "plot_lattice_network",
    "plot_phase_space",
    # Integration utilities
    "states_to_array",
    "lattice_to_array",
    "states_to_dataframe",
    "lattice_to_dataframe",
    "batch_project_forward",
    "compute_statistics",
]
