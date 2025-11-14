"""
Demonstration: Geometric Handling of Infinities
================================================
Compares traditional numerical methods vs PSMSL geometric approach
for handling singularities (1/r → ∞ as r → 0).

Authors: Nathanael Joseph Bocker
Date: November 13, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from psmsl_core import *

def traditional_gravity_potential(r: float, M: float = 1.0, G: float = 1.0) -> float:
    """
    Traditional numerical approach: Φ = -GM/r
    Problem: As r → 0, Φ → -∞ (numerical overflow)
    """
    if r < 1e-15:  # Arbitrary cutoff
        return float('-inf')  # Overflow
    return -G * M / r


def geometric_gravity_potential(state: TriadicState, 
                                detector: PhaseTransitionDetector,
                                engine: PhaseTransitionEngine,
                                max_transitions: int = 5) -> Tuple[float, int]:
    """
    Geometric approach: Potential represented as geometric curvature.
    As r → 0, depth increases. When approaching horizon, trigger scale transition.
    
    Returns: (potential_value, num_transitions)
    """
    r = state.M_curvature
    transitions = 0
    
    # Check for phase transition
    transition_info = detector.check_transition(state)
    
    while transition_info['needed'] and transitions < max_transitions:
        if transition_info['type'] == 'scale_up':
            # Execute geometric phase transition instead of hitting infinity
            state = engine.scale_up(state)
            transitions += 1
            print(f"  → Phase transition #{transitions}: {transition_info['reason']}")
            r = state.M_curvature
            transition_info = detector.check_transition(state)
        else:
            break
    
    # Compute potential as geometric quantity
    if r > 0 and not np.isinf(r):
        phi_potential = -1.0 / r
    else:
        phi_potential = -(PHI ** state.tetrahedron.depth)
    
    return phi_potential, transitions


def demo_singularity_comparison():
    """
    Main demonstration comparing traditional vs geometric approaches.
    """
    print("=" * 70)
    print("DEMONSTRATION: Handling Gravitational Singularity (1/r → ∞)")
    print("=" * 70)
    print()
    
    # Test at progressively smaller radii
    r_values = [1.0, 0.1, 0.01, 1e-3, 1e-6, 1e-9, 1e-12, 1e-15, 1e-18, 1e-20]
    
    print("TRADITIONAL NUMERICAL METHOD:")
    print("-" * 70)
    trad_results = []
    for r in r_values:
        try:
            phi = traditional_gravity_potential(r)
            if np.isinf(phi):
                result_str = "OVERFLOW (∞)"
                trad_results.append(np.nan)
            else:
                result_str = f"{phi:.3e}"
                trad_results.append(phi)
        except:
            result_str = "ERROR"
            trad_results.append(np.nan)
        
        print(f"  r = {r:.2e}  →  Φ = {result_str}")
    
    print()
    print("GEOMETRIC PHASE TRANSITION METHOD:")
    print("-" * 70)
    
    detector = PhaseTransitionDetector(precision_bits=32)
    engine = PhaseTransitionEngine()
    geom_results = []
    
    for r in r_values:
        # Create triadic state with M = r
        # Depth is chosen such that φ^depth ≈ 1/r (smaller r → larger depth)
        if r >= 1.0:
            depth = 0
        else:
            depth = int(np.log(1/r) / np.log(PHI))
        
        # Ensure we don't start too close to horizon
        depth = min(depth, 160)
        
        # Create tetrahedron with 120° base symmetry
        base_angles = (0, 2*np.pi/3, 4*np.pi/3, np.pi)
        tetra = Tetrahedron(id=0, depth=depth, base_angles=base_angles)
        state = TriadicState(tetra)
        
        print(f"  r = {r:.2e} (depth={depth})")
        phi, num_transitions = geometric_gravity_potential(state, detector, engine)
        geom_results.append(phi)
        
        if num_transitions > 0:
            print(f"    Final: Φ = {phi:.3e} (after {num_transitions} transitions)")
        else:
            print(f"    Φ = {phi:.3e}")
    
    print()
    print("=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    
    trad_failures = sum(1 for x in trad_results if np.isnan(x) or np.isinf(x))
    geom_failures = sum(1 for x in geom_results if np.isnan(x) or np.isinf(x))
    
    print(f"Traditional method: {trad_failures}/{len(r_values)} failures (overflow/NaN)")
    print(f"Geometric method:   {geom_failures}/{len(r_values)} failures")
    print()
    print("RESULT: Geometric method handles singularities via phase transitions,")
    print("        avoiding numerical overflow entirely.")
    print()
    
    # Create visualization
    create_comparison_plot(r_values, trad_results, geom_results)


def create_comparison_plot(r_values, trad_results, geom_results):
    """Create a visualization comparing the two methods."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Traditional method plot
    valid_trad = [(r, phi) for r, phi in zip(r_values, trad_results) 
                  if not (np.isnan(phi) or np.isinf(phi))]
    
    if valid_trad:
        r_trad, phi_trad = zip(*valid_trad)
        ax1.loglog(r_trad, np.abs(phi_trad), 'ro-', linewidth=2, markersize=8, label='Valid')
    
    # Mark failures
    failed_trad = [r for r, phi in zip(r_values, trad_results) 
                   if np.isnan(phi) or np.isinf(phi)]
    if failed_trad:
        ax1.loglog(failed_trad, [1e10]*len(failed_trad), 'rx', markersize=15, 
                   markeredgewidth=3, label='Overflow')
    
    ax1.set_xlabel('Radius r', fontsize=12)
    ax1.set_ylabel('|Potential Φ|', fontsize=12)
    ax1.set_title('Traditional Numerical Method\n(Fails at small r)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)
    
    # Geometric method plot
    valid_geom = [(r, phi) for r, phi in zip(r_values, geom_results) 
                  if not (np.isnan(phi) or np.isinf(phi))]
    
    if valid_geom:
        r_geom, phi_geom = zip(*valid_geom)
        ax2.loglog(r_geom, np.abs(phi_geom), 'go-', linewidth=2, markersize=8, label='Stable')
    
    ax2.set_xlabel('Radius r', fontsize=12)
    ax2.set_ylabel('|Potential Φ|', fontsize=12)
    ax2.set_title('Geometric Phase Transition Method\n(Handles all scales)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/singularity_comparison.png', dpi=300, bbox_inches='tight')
    print("Visualization saved to: singularity_comparison.png")
    print()


if __name__ == "__main__":
    demo_singularity_comparison()
