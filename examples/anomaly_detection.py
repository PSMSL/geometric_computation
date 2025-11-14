"""
Practical Application: Anomaly Detection in Time Series Data
==============================================================

This example demonstrates how PSMSL's geometric approach naturally detects
anomalies in time series data by measuring entropy (mirror drift).

Use Case: Detecting unusual patterns in sensor data, financial transactions,
network traffic, or any sequential data stream.

Authors: Nathanael Joseph Bocker and Manus AI
Date: November 13, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from libpsmsl import Tetrahedron, TriadicState, GeometricLattice, plot_triadic_properties

def generate_time_series_with_anomaly(n_points=100, anomaly_position=50, anomaly_magnitude=5):
    """
    Generate a synthetic time series with a deliberate anomaly.
    
    Args:
        n_points: Number of data points
        anomaly_position: Where to inject the anomaly
        anomaly_magnitude: How severe the anomaly is
    
    Returns:
        Array of time series values
    """
    # Normal data: sine wave with noise
    t = np.linspace(0, 4*np.pi, n_points)
    normal_data = np.sin(t) + 0.1 * np.random.randn(n_points)
    
    # Inject anomaly
    normal_data[anomaly_position] += anomaly_magnitude
    
    return normal_data


def detect_anomalies_with_psmsl(data, threshold=2.0):
    """
    Use PSMSL to detect anomalies by measuring entropy (mirror drift).
    
    The key insight: Anomalies create geometric inconsistencies that manifest
    as high entropy (large mirror drift).
    
    Args:
        data: Time series data
        threshold: Entropy threshold for anomaly detection (in std deviations)
    
    Returns:
        List of anomaly indices, list of entropy values
    """
    lattice = GeometricLattice()
    entropies = []
    
    # Create a lattice where each data point becomes a tetrahedron
    # The base angles are derived from the data values
    for i, value in enumerate(data):
        # Map data value to base angles (normalize to 0-360 range)
        normalized_value = (value - data.min()) / (data.max() - data.min())
        base_angle = normalized_value * 360
        
        # Create tetrahedron with angles derived from data
        tid = lattice.add_tetrahedron(depth=0, base_angles=(base_angle, base_angle+120, base_angle+240, base_angle+360))
        
        # Connect to previous tetrahedron (creating a chain)
        if i > 0:
            lattice.connect(tid-1, 0, tid, 0)
    
    # Compute entropy for each tetrahedron
    for tid in sorted(lattice.tetrahedra.keys()):
        entropy = lattice.states[tid].sigma_entropy
        entropies.append(entropy)
    
    # Detect anomalies: points where entropy exceeds threshold
    entropies = np.array(entropies)
    mean_entropy = np.mean(entropies)
    std_entropy = np.std(entropies)
    
    anomaly_indices = np.where(entropies > mean_entropy + threshold * std_entropy)[0]
    
    return anomaly_indices, entropies


def demo_anomaly_detection():
    """
    Run the anomaly detection demonstration.
    """
    print("=" * 70)
    print("PRACTICAL APPLICATION: Anomaly Detection with PSMSL")
    print("=" * 70)
    print()
    print("Scenario: Detecting unusual spikes in sensor data")
    print()
    
    # Generate data with a known anomaly
    data = generate_time_series_with_anomaly(n_points=100, anomaly_position=50, anomaly_magnitude=5)
    
    print("Step 1: Generated time series with anomaly at position 50")
    print(f"  Data range: [{data.min():.2f}, {data.max():.2f}]")
    print()
    
    # Detect anomalies
    print("Step 2: Creating geometric lattice from data...")
    anomaly_indices, entropies = detect_anomalies_with_psmsl(data, threshold=2.0)
    print(f"  Created lattice with {len(data)} tetrahedra")
    print()
    
    print("Step 3: Analyzing entropy (mirror drift) for anomalies...")
    print(f"  Mean entropy: {np.mean(entropies):.6f}")
    print(f"  Std entropy: {np.std(entropies):.6f}")
    print()
    
    print("=" * 70)
    print("RESULTS:")
    print("=" * 70)
    print(f"Detected {len(anomaly_indices)} anomalies at positions: {anomaly_indices.tolist()}")
    print()
    
    if 50 in anomaly_indices:
        print("✓ SUCCESS: The injected anomaly at position 50 was correctly detected!")
    else:
        print("⚠ The injected anomaly was not detected. Try adjusting the threshold.")
    
    print()
    print("KEY INSIGHT:")
    print("  Anomalies create geometric inconsistencies in the lattice.")
    print("  These inconsistencies manifest as high entropy (mirror drift).")
    print("  No machine learning training required—it's purely geometric!")
    print()
    
    # Visualize results
    create_visualization(data, entropies, anomaly_indices)


def create_visualization(data, entropies, anomaly_indices):
    """
    Create a visualization of the anomaly detection results.
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Original time series with detected anomalies
    axes[0].plot(data, 'b-', linewidth=2, label='Time Series Data')
    axes[0].scatter(anomaly_indices, data[anomaly_indices], c='r', s=200, 
                    marker='X', label='Detected Anomalies', zorder=5, edgecolors='black', linewidths=2)
    axes[0].set_xlabel('Time Step', fontsize=12)
    axes[0].set_ylabel('Value', fontsize=12)
    axes[0].set_title('Time Series with Detected Anomalies', fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Entropy over time
    axes[1].plot(entropies, 'g-', linewidth=2, label='Entropy (Mirror Drift)')
    axes[1].axhline(y=np.mean(entropies) + 2*np.std(entropies), color='r', 
                    linestyle='--', linewidth=2, label='Anomaly Threshold', alpha=0.7)
    axes[1].scatter(anomaly_indices, entropies[anomaly_indices], c='r', s=200, 
                    marker='X', zorder=5, edgecolors='black', linewidths=2)
    axes[1].set_xlabel('Time Step', fontsize=12)
    axes[1].set_ylabel('Entropy (σ)', fontsize=12)
    axes[1].set_title('Geometric Entropy: High Values Indicate Anomalies', fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/psmsl-project/examples/anomaly_detection_result.png', dpi=300, bbox_inches='tight')
    print("Visualization saved to: examples/anomaly_detection_result.png")
    print()


if __name__ == "__main__":
    demo_anomaly_detection()
