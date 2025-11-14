"""
Unit tests for PSMSL core functionality
"""

import pytest
import numpy as np
from libpsmsl import (
    PHI,
    TensorFace,
    Tetrahedron,
    TriadicState,
    GeometricLattice,
    states_to_array,
    compute_statistics,
)


class TestTensorFace:
    """Tests for the TensorFace class"""
    
    def test_initialization(self):
        """Test that TensorFace initializes correctly"""
        face = TensorFace(face_id=0, depth=0, base_angle=0.0)
        assert face.face_id == 0
        assert face.depth == 0
        assert face.base_angle == 0.0
        assert face.matrix.shape == (2, 2)
    
    def test_phase_calculation(self):
        """Test phase angle calculation"""
        face = TensorFace(face_id=0, depth=0, base_angle=np.pi/2)
        phase = face.get_phase()
        assert np.isclose(phase, np.pi/2)
    
    def test_norm(self):
        """Test Frobenius norm calculation"""
        face = TensorFace(face_id=0, depth=0, base_angle=0.0)
        norm = face.get_norm()
        assert norm >= 0
    
    def test_rotation(self):
        """Test rotation operation"""
        face = TensorFace(face_id=0, depth=0, base_angle=0.0)
        original_matrix = face.matrix.copy()
        face.rotate(np.pi/4)
        # Matrix should have changed
        assert not np.allclose(face.matrix, original_matrix)


class TestTetrahedron:
    """Tests for the Tetrahedron class"""
    
    def test_initialization(self):
        """Test that Tetrahedron initializes correctly"""
        tetra = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        assert tetra.id == 0
        assert tetra.depth == 0
        assert len(tetra.faces) == 4
    
    def test_phi_scaling(self):
        """Test φ-scaling operation"""
        tetra = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        scaled = tetra.scale_up()
        assert scaled.depth == tetra.depth + 1
    
    def test_mirror_generation(self):
        """Test mirror tetrahedron generation"""
        tetra = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        mirror = tetra.get_mirror()
        assert mirror is not None
        assert len(mirror.faces) == 4


class TestTriadicState:
    """Tests for the TriadicState class"""
    
    def test_initialization(self):
        """Test that TriadicState initializes correctly"""
        tetra = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        state = TriadicState(tetra)
        assert state.tetrahedron == tetra
    
    def test_properties_are_finite(self):
        """Test that all triadic properties are finite"""
        tetra = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        state = TriadicState(tetra)
        
        assert np.isfinite(state.T_persistence)
        assert np.isfinite(state.M_curvature)
        assert np.isfinite(state.rho_E_flux)
        assert np.isfinite(state.sigma_entropy)
    
    def test_projection_forward(self):
        """Test forward projection"""
        tetra = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        state = TriadicState(tetra)
        next_state = state.project_forward()
        
        assert next_state.tetrahedron.depth == state.tetrahedron.depth + 1
        assert next_state.previous_state == state


class TestGeometricLattice:
    """Tests for the GeometricLattice class"""
    
    def test_initialization(self):
        """Test that GeometricLattice initializes correctly"""
        lattice = GeometricLattice(dimension=3)
        assert lattice.dimension == 3
        assert len(lattice) == 0
    
    def test_add_tetrahedron(self):
        """Test adding tetrahedra to the lattice"""
        lattice = GeometricLattice()
        tid = lattice.add_tetrahedron()
        assert tid == 0
        assert len(lattice) == 1
        assert tid in lattice.tetrahedra
    
    def test_connection(self):
        """Test connecting two tetrahedra"""
        lattice = GeometricLattice()
        tid1 = lattice.add_tetrahedron()
        tid2 = lattice.add_tetrahedron()
        
        lattice.connect(tid1, 0, tid2, 0)
        neighbors1 = lattice.get_neighbors(tid1)
        neighbors2 = lattice.get_neighbors(tid2)
        
        assert neighbors1[0] == tid2
        assert neighbors2[0] == tid1
    
    def test_evolve_all(self):
        """Test evolving all tetrahedra"""
        lattice = GeometricLattice()
        lattice.add_tetrahedron(depth=0)
        lattice.add_tetrahedron(depth=0)
        
        initial_depths = [t.depth for t in lattice.tetrahedra.values()]
        lattice.evolve_all()
        final_depths = [t.depth for t in lattice.tetrahedra.values()]
        
        assert all(f == i + 1 for i, f in zip(initial_depths, final_depths))
    
    def test_global_entropy(self):
        """Test global entropy calculation"""
        lattice = GeometricLattice()
        lattice.add_tetrahedron()
        lattice.add_tetrahedron()
        
        entropy = lattice.compute_global_entropy()
        assert np.isfinite(entropy)
        assert entropy >= 0
    
    def test_save_load(self, tmp_path):
        """Test saving and loading lattice"""
        lattice = GeometricLattice()
        tid1 = lattice.add_tetrahedron(depth=0)
        tid2 = lattice.add_tetrahedron(depth=1)
        lattice.connect(tid1, 0, tid2, 0)
        
        filepath = tmp_path / "test_lattice.json"
        lattice.save(str(filepath))
        
        loaded_lattice = GeometricLattice.load(str(filepath))
        assert len(loaded_lattice) == len(lattice)
        assert loaded_lattice.tetrahedra[tid1].depth == lattice.tetrahedra[tid1].depth


class TestIntegration:
    """Tests for integration utilities"""
    
    def test_states_to_array(self):
        """Test converting states to NumPy array"""
        tetra1 = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        tetra2 = Tetrahedron(id=1, depth=1, base_angles=(0, 120, 240, 360))
        states = [TriadicState(tetra1), TriadicState(tetra2)]
        
        arr = states_to_array(states)
        assert arr.shape == (2, 4)
        assert np.all(np.isfinite(arr))
    
    def test_compute_statistics(self):
        """Test statistical computation"""
        tetra1 = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        tetra2 = Tetrahedron(id=1, depth=1, base_angles=(0, 120, 240, 360))
        states = [TriadicState(tetra1), TriadicState(tetra2)]
        
        stats = compute_statistics(states)
        assert 'T' in stats
        assert 'mean' in stats['T']
        assert np.isfinite(stats['T']['mean'])


class TestPhysicalConsistency:
    """Tests for physical consistency and conservation laws"""
    
    def test_no_overflow_at_large_depth(self):
        """Test that large depths don't cause overflow"""
        tetra = Tetrahedron(id=0, depth=100, base_angles=(0, 120, 240, 360))
        state = TriadicState(tetra)
        
        assert np.isfinite(state.T_persistence)
        assert np.isfinite(state.M_curvature)
        assert np.isfinite(state.rho_E_flux)
        assert np.isfinite(state.sigma_entropy)
    
    def test_phi_scaling_consistency(self):
        """Test that φ-scaling is consistent"""
        tetra1 = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))
        tetra2 = tetra1.scale_up()
        
        ratio = tetra2.depth / (tetra1.depth + 1)
        assert np.isclose(ratio, 1.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
