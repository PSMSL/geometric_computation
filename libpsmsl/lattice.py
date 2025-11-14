"""
PSMSL Lattice: Geometric Lattice Management
============================================
Manages collections of interconnected tetrahedra in geometric space.

Copyright 2025 Nathanael Joseph Bocker and contributors
Licensed under the Apache License, Version 2.0
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import json
from .psmsl_core import Tetrahedron, TriadicState, PHI


class GeometricLattice:
    """
    A lattice of interconnected tetrahedra forming a computational mesh.
    
    Each tetrahedron can have up to 4 neighbors (one per face).
    The lattice manages connectivity, boundary conditions, and collective operations.
    """
    
    def __init__(self, dimension: int = 3):
        """
        Initialize an empty geometric lattice.
        
        Args:
            dimension: Spatial dimension (default 3 for physical space)
        """
        self.dimension = dimension
        self.tetrahedra: Dict[int, Tetrahedron] = {}
        self.states: Dict[int, TriadicState] = {}
        self.connectivity: Dict[int, Dict[int, Optional[int]]] = {}  # {tetra_id: {face_id: neighbor_id}}
        self._next_id = 0
    
    def add_tetrahedron(self, depth: int = 0, base_angles: Optional[Tuple[float, ...]] = None) -> int:
        """
        Add a new tetrahedron to the lattice.
        
        Args:
            depth: Initial depth (scale) of the tetrahedron
            base_angles: Base angles for the four faces (default: 0, 120, 240, 360)
        
        Returns:
            The ID of the newly created tetrahedron
        """
        if base_angles is None:
            base_angles = (0, 120, 240, 360)
        
        tetra_id = self._next_id
        self._next_id += 1
        
        tetra = Tetrahedron(tetra_id, depth, base_angles)
        state = TriadicState(tetra)
        
        self.tetrahedra[tetra_id] = tetra
        self.states[tetra_id] = state
        self.connectivity[tetra_id] = {0: None, 1: None, 2: None, 3: None}
        
        return tetra_id
    
    def connect(self, tetra_id_1: int, face_id_1: int, tetra_id_2: int, face_id_2: int):
        """
        Create a bidirectional connection between two tetrahedra.
        
        Args:
            tetra_id_1: ID of the first tetrahedron
            face_id_1: Face ID on the first tetrahedron (0-3)
            tetra_id_2: ID of the second tetrahedron
            face_id_2: Face ID on the second tetrahedron (0-3)
        """
        if tetra_id_1 not in self.tetrahedra or tetra_id_2 not in self.tetrahedra:
            raise ValueError("Both tetrahedra must exist in the lattice")
        
        if face_id_1 not in range(4) or face_id_2 not in range(4):
            raise ValueError("Face IDs must be in range 0-3")
        
        self.connectivity[tetra_id_1][face_id_1] = tetra_id_2
        self.connectivity[tetra_id_2][face_id_2] = tetra_id_1
    
    def get_neighbors(self, tetra_id: int) -> List[Optional[int]]:
        """
        Get the IDs of all neighboring tetrahedra.
        
        Args:
            tetra_id: ID of the tetrahedron
        
        Returns:
            List of neighbor IDs (None for unconnected faces)
        """
        if tetra_id not in self.connectivity:
            raise ValueError(f"Tetrahedron {tetra_id} not found in lattice")
        
        return [self.connectivity[tetra_id][i] for i in range(4)]
    
    def evolve_all(self):
        """
        Evolve all tetrahedra in the lattice by one time step (φ-projection).
        """
        new_states = {}
        for tetra_id, state in self.states.items():
            new_states[tetra_id] = state.project_forward()
        
        self.states = new_states
        for tetra_id, state in self.states.items():
            self.tetrahedra[tetra_id] = state.tetrahedron
    
    def compute_global_entropy(self) -> float:
        """
        Compute the total entropy (mirror drift) across the entire lattice.
        
        Returns:
            Sum of all individual tetrahedron entropies
        """
        return sum(state.sigma_entropy for state in self.states.values())
    
    def compute_average_properties(self) -> Dict[str, float]:
        """
        Compute average values of the triadic properties across the lattice.
        
        Returns:
            Dictionary with average T, M, ρ_E, and σ
        """
        if not self.states:
            return {"T": 0.0, "M": 0.0, "rho_E": 0.0, "sigma": 0.0}
        
        n = len(self.states)
        return {
            "T": sum(s.T_persistence for s in self.states.values()) / n,
            "M": sum(s.M_curvature for s in self.states.values()) / n,
            "rho_E": sum(s.rho_E_flux for s in self.states.values()) / n,
            "sigma": sum(s.sigma_entropy for s in self.states.values()) / n,
        }
    
    def to_dict(self) -> dict:
        """
        Serialize the lattice to a dictionary.
        
        Returns:
            Dictionary representation of the lattice
        """
        return {
            "dimension": self.dimension,
            "tetrahedra": {
                str(tid): {
                    "depth": tetra.depth,
                    "base_angles": tetra.get_base_angles(),
                }
                for tid, tetra in self.tetrahedra.items()
            },
            "connectivity": {
                str(tid): {str(fid): nid for fid, nid in conn.items()}
                for tid, conn in self.connectivity.items()
            },
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GeometricLattice':
        """
        Deserialize a lattice from a dictionary.
        
        Args:
            data: Dictionary representation of the lattice
        
        Returns:
            Reconstructed GeometricLattice object
        """
        lattice = cls(dimension=data["dimension"])
        
        # Recreate tetrahedra
        for tid_str, tetra_data in data["tetrahedra"].items():
            tid = int(tid_str)
            lattice._next_id = max(lattice._next_id, tid + 1)
            
            tetra = Tetrahedron(tid, tetra_data["depth"], tuple(tetra_data["base_angles"]))
            state = TriadicState(tetra)
            
            lattice.tetrahedra[tid] = tetra
            lattice.states[tid] = state
        
        # Recreate connectivity
        for tid_str, conn_data in data["connectivity"].items():
            tid = int(tid_str)
            lattice.connectivity[tid] = {
                int(fid): (int(nid) if nid is not None else None)
                for fid, nid in conn_data.items()
            }
        
        return lattice
    
    def save(self, filename: str):
        """
        Save the lattice to a JSON file.
        
        Args:
            filename: Path to the output file
        """
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filename: str) -> 'GeometricLattice':
        """
        Load a lattice from a JSON file.
        
        Args:
            filename: Path to the input file
        
        Returns:
            Loaded GeometricLattice object
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def __len__(self) -> int:
        """Return the number of tetrahedra in the lattice."""
        return len(self.tetrahedra)
    
    def __repr__(self) -> str:
        return f"GeometricLattice(dimension={self.dimension}, tetrahedra={len(self)})"
