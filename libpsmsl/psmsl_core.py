"""
PSMSL Core: Geometric Computational Model
==========================================
Implementation of the Projected Symmetry Mirrored Semantic Lattice
that handles infinities and imaginary numbers geometrically.

Authors: Nathanael Joseph Bocker and Manus AI
Date: November 13, 2025
"""

import numpy as np
from typing import Optional, Tuple, List
import warnings
warnings.filterwarnings('ignore')

# Golden ratio - the fundamental scaling constant
PHI = (1 + np.sqrt(5)) / 2

class TensorFace:
    """
    A 2x2 real-valued tensor representing a face of the computational tetrahedron.
    Encodes local directional information (gradients, shear, rotation).
    """
    
    def __init__(self, face_id: int, depth: int, base_angle: float):
        self.face_id = face_id
        self.depth = depth
        self.base_angle = base_angle
        
        # Calculate phase angle with φ-scaling
        theta = (base_angle * (PHI ** depth)) % (2 * np.pi)
        
        # Initialize as antisymmetric matrix
        self.matrix = np.array([
            [np.sin(theta), -np.sin(theta)],
            [-np.sin(theta), np.sin(theta)]
        ], dtype=np.float64)
    
    def get_phase(self) -> float:
        """Calculate the current phase angle."""
        return (self.base_angle * (PHI ** self.depth)) % (2 * np.pi)
    
    def get_norm(self) -> float:
        """Calculate the Frobenius norm of the matrix."""
        return np.linalg.norm(self.matrix, 'fro')
    
    def rotate(self, angle: float):
        """Apply a 2D rotation to the tensor face (for imaginary number handling)."""
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        self.matrix = rotation_matrix @ self.matrix
    
    def mirror(self) -> np.ndarray:
        """Return the mirror (negation) of this face."""
        return -self.matrix
    
    def copy(self):
        """Create a deep copy of this tensor face."""
        new_face = TensorFace(self.face_id, self.depth, self.base_angle)
        new_face.matrix = self.matrix.copy()
        return new_face


class Tetrahedron:
    """
    The fundamental computational unit - a geometric "bit".
    Contains four tensor faces arranged in tetrahedral geometry.
    """
    
    def __init__(self, id: int, depth: int, base_angles: Tuple[float, float, float, float]):
        self.id = id
        self.depth = depth
        self.radius = PHI ** depth  # R_n = φ^n
        
        # Create four tensor faces with 120° base symmetry (plus one for 4th dimension)
        self.faces = [
            TensorFace(i, depth, base_angles[i]) 
            for i in range(4)
        ]
        
        self._mirror_cache = None
    
    def create_mirror(self):
        """Generate the mirrored version of this tetrahedron."""
        mirror_tetra = Tetrahedron(self.id, self.depth, self.get_base_angles())
        for i, face in enumerate(self.faces):
            mirror_tetra.faces[i].matrix = face.mirror()
        self._mirror_cache = mirror_tetra
        return mirror_tetra
    
    def get_base_angles(self) -> Tuple[float, float, float, float]:
        """Extract the base angles from the faces."""
        return tuple(face.base_angle for face in self.faces)
    
    def copy(self):
        """Create a deep copy of this tetrahedron."""
        new_tetra = Tetrahedron(self.id, self.depth, self.get_base_angles())
        new_tetra.faces = [face.copy() for face in self.faces]
        return new_tetra


class TriadicState:
    """
    Physical interpretation of a tetrahedron's geometry.
    Maps geometric properties to physical currencies: T, M, ρ_E, σ.
    """
    
    def __init__(self, tetrahedron: Tetrahedron):
        self.tetrahedron = tetrahedron
        self._previous_state = None
    
    @property
    def T_persistence(self) -> float:
        """Time/Persistence: Average phase coherence."""
        phases = [face.get_phase() for face in self.tetrahedron.faces]
        return np.mean(phases)
    
    @property
    def M_curvature(self) -> float:
        """Mass/Curvature: Radial scale factor."""
        return self.tetrahedron.radius
    
    @property
    def rho_flux(self) -> float:
        """Energy Density/Flux: Rate of tensor change."""
        if self._previous_state is None:
            return 0.0
        
        # Calculate rate of change of tensor norms
        current_norms = [face.get_norm() for face in self.tetrahedron.faces]
        previous_norms = [face.get_norm() for face in self._previous_state.tetrahedron.faces]
        
        changes = [abs(c - p) for c, p in zip(current_norms, previous_norms)]
        return np.mean(changes)
    
    @property
    def sigma_entropy(self) -> float:
        """Entropy gap: Mirror drift."""
        if self.tetrahedron._mirror_cache is None:
            self.tetrahedron.create_mirror()
        
        # Calculate drift δ(F, F*) = Σ|F_ij + F*_ij|
        total_drift = 0.0
        for face, mirror_face in zip(self.tetrahedron.faces, 
                                      self.tetrahedron._mirror_cache.faces):
            drift = np.sum(np.abs(face.matrix + mirror_face.matrix))
            total_drift += drift
        
        return total_drift / 4.0  # Average over all faces
    
    def set_previous_state(self, prev_state):
        """Set the previous state for flux calculation."""
        self._previous_state = prev_state
    
    def project_forward(self):
        """Project the state forward by one φ-scaling step."""
        # Create a new tetrahedron at the next depth
        base_angles = self.tetrahedron.get_base_angles()
        new_tetra = Tetrahedron(
            id=self.tetrahedron.id,
            depth=self.tetrahedron.depth + 1,
            base_angles=base_angles
        )
        new_state = TriadicState(new_tetra)
        new_state.set_previous_state(self)
        return new_state
    
    @property
    def previous_state(self):
        """Get the previous state."""
        return self._previous_state


class PhaseTransitionDetector:
    """
    Monitors system state and detects when phase transitions are needed.
    """
    
    def __init__(self, precision_bits: int = 32):
        self.precision_bits = precision_bits
        self.phi_horizon = self._calculate_horizon()
        self.entropy_threshold = 1.0
    
    def _calculate_horizon(self) -> int:
        """
        Calculate φ^n horizon based on floating-point precision.
        32-bit: φ^173 ≈ 1.4 × 10^18
        64-bit: φ^362 ≈ 1.6 × 10^38
        """
        if self.precision_bits == 32:
            return 173
        elif self.precision_bits == 64:
            return 362
        else:
            mantissa_digits = self.precision_bits * 0.30103
            return int(np.log(10 ** mantissa_digits) / np.log(PHI))
    
    def check_transition(self, state: TriadicState) -> dict:
        """
        Check if a phase transition is needed.
        
        Returns:
            dict with 'needed', 'type', and 'reason' keys
        """
        depth = state.tetrahedron.depth
        sigma = state.sigma_entropy
        
        # Check 1: Approaching φ-horizon (infinity)
        if depth >= self.phi_horizon - 10:
            return {
                'needed': True,
                'type': 'scale_up',
                'reason': f'Approaching φ-horizon at depth {depth}'
            }
        
        # Check 2: High entropy (decoherence)
        if sigma > self.entropy_threshold:
            return {
                'needed': True,
                'type': 'entropy_forcing',
                'reason': f'Entropy gap σ = {sigma:.3f} exceeds threshold'
            }
        
        # Check 3: NaN detection (precision collapse)
        if np.isnan(sigma):
            return {
                'needed': True,
                'type': 'scale_down',
                'reason': 'Precision collapse detected (NaN in drift)'
            }
        
        return {
            'needed': False,
            'type': None,
            'reason': 'System coherent'
        }


class PhaseTransitionEngine:
    """
    Executes geometric phase transitions when infinities are approached.
    """
    
    def scale_up(self, state: TriadicState, jump_size: int = 50) -> TriadicState:
        """
        Transition to larger scale (zoom out).
        Used when approaching infinity (r → 0, depth → horizon).
        """
        old_depth = state.tetrahedron.depth
        new_depth = max(0, old_depth - jump_size)
        scale_factor = PHI ** (old_depth - new_depth)
        
        # Create new tetrahedron at lower depth
        new_tetra = Tetrahedron(
            id=state.tetrahedron.id,
            depth=new_depth,
            base_angles=state.tetrahedron.get_base_angles()
        )
        
        # Rescale tensor faces to preserve physical meaning
        for i, face in enumerate(new_tetra.faces):
            face.matrix *= scale_factor
        
        new_state = TriadicState(new_tetra)
        new_state.set_previous_state(state)
        
        return new_state
    
    def scale_down(self, state: TriadicState, jump_size: int = 10) -> TriadicState:
        """
        Transition to smaller scale (zoom in).
        Used when precision collapse is detected.
        """
        old_depth = state.tetrahedron.depth
        new_depth = old_depth + jump_size
        
        new_tetra = Tetrahedron(
            id=state.tetrahedron.id,
            depth=new_depth,
            base_angles=state.tetrahedron.get_base_angles()
        )
        
        # Renormalize to prevent overflow
        for face in new_tetra.faces:
            face.matrix /= (PHI ** jump_size)
        
        new_state = TriadicState(new_tetra)
        new_state.set_previous_state(state)
        
        return new_state
    
    def entropy_forcing(self, state: TriadicState) -> TriadicState:
        """
        Apply entropy forcing when σ exceeds threshold.
        Adjusts triadic angles to restore symmetry.
        """
        sigma = state.sigma_entropy
        
        # Determine forcing direction
        if sigma > 1.0:  # High entropy → force expansion
            angle_adjustment = 5 * (np.pi / 180)  # +5 degrees
        else:  # Low entropy → force compression
            angle_adjustment = -5 * (np.pi / 180)  # -5 degrees
        
        # Create new tetrahedron with adjusted geometry
        old_angles = state.tetrahedron.get_base_angles()
        new_angles = tuple(angle + angle_adjustment for angle in old_angles)
        
        new_tetra = Tetrahedron(
            id=state.tetrahedron.id,
            depth=state.tetrahedron.depth,
            base_angles=new_angles
        )
        
        new_state = TriadicState(new_tetra)
        new_state.set_previous_state(state)
        
        return new_state


def handle_imaginary_via_rotation(state: TriadicState, imaginary_component: float) -> TriadicState:
    """
    Handle imaginary numbers geometrically via rotation.
    Instead of storing a + bi, we store magnitude and phase.
    """
    # Convert to polar form
    real_component = state.M_curvature
    magnitude = np.sqrt(real_component**2 + imaginary_component**2)
    phase = np.arctan2(imaginary_component, real_component)
    
    # Create new state with rotated geometry
    new_tetra = state.tetrahedron.copy()
    
    # Apply rotation to all faces
    for face in new_tetra.faces:
        face.rotate(phase)
    
    new_state = TriadicState(new_tetra)
    new_state.set_previous_state(state)
    
    return new_state


if __name__ == "__main__":
    print("PSMSL Core Module Loaded Successfully")
    print(f"Golden Ratio φ = {PHI:.10f}")
    print(f"32-bit φ-horizon: φ^173 = {PHI**173:.3e}")
    print(f"64-bit φ-horizon: φ^362 = {PHI**362:.3e}")
