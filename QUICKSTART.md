# PSMSL Quick Start Guide

Welcome to PSMSL! This guide will get you up and running in under 5 minutes.

## Installation

### Option 1: Clone and Install (Recommended for Development)

```bash
git clone https://github.com/your-repo/psmsl.git
cd psmsl
pip install -e .
```

The `-e` flag installs the package in "editable" mode, meaning changes you make to the code will immediately be reflected without reinstalling.

### Option 2: Install from Source

```bash
git clone https://github.com/your-repo/psmsl.git
cd psmsl
pip install .
```

### Option 3: Install from PyPI (Coming Soon)

```bash
pip install psmsl
```

## Your First PSMSL Program

Create a file called `my_first_geometric_computation.py`:

```python
from libpsmsl import Tetrahedron, TriadicState, PHI

# Create a tetrahedron at depth 0 (the "origin" of geometric space)
tetra = Tetrahedron(id=0, depth=0, base_angles=(0, 120, 240, 360))

# Wrap it in a TriadicState to access physical interpretations
state = TriadicState(tetra)

# Compute the emergent properties
print(f"Time (Persistence): {state.T_persistence:.6f}")
print(f"Mass (Curvature): {state.M_curvature:.6f}")
print(f"Energy Density (Flux): {state.rho_E_flux:.6f}")
print(f"Entropy (Mirror Drift): {state.sigma_entropy:.6f}")

# Project to the next scale (φ-scaling)
next_state = state.project_forward()
print(f"\nAfter projection:")
print(f"New depth: {next_state.tetrahedron.depth}")
print(f"Scale factor: {PHI}")
```

Run it:

```bash
python my_first_geometric_computation.py
```

You've just performed a geometric computation!

## Run the Demonstrations

### Demo 1: Handling Infinities

See how PSMSL handles singularities without overflow:

```bash
python demos/demo_infinities.py
```

This will generate a visualization (`singularity_comparison.png`) showing the traditional method failing while the geometric method remains stable.

### Demo 2: Handling Imaginary Numbers

See how complex arithmetic is replaced by geometric rotation:

```bash
python demos/demo_imaginary_fixed.py
```

This will generate a visualization (`imaginary_comparison_fixed.png`) showing that the geometric method produces identical results to traditional complex arithmetic.

## Next Steps

-   **Read the Theory:** Check out [`docs/unified_theory.md`](./docs/unified_theory.md) to understand the physics behind PSMSL.
-   **Explore the Code:** The core library is in [`libpsmsl/psmsl_core.py`](./libpsmsl/psmsl_core.py). It's well-commented and designed to be readable.
-   **Build Something:** Use PSMSL in your own projects. We'd love to hear what you create!
-   **Contribute:** See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to get involved.

## Getting Help

-   **Documentation:** See the [`docs/`](./docs/) directory
-   **Issues:** Report bugs or request features on [GitHub Issues](https://github.com/your-repo/psmsl/issues)
-   **Discussions:** Join the conversation on [GitHub Discussions](https://github.com/your-repo/psmsl/discussions)

Welcome to the geometric computing revolution!
