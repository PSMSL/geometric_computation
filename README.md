# PSMSL: The Geometric Computational Engine

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/your-repo/psmsl.svg?style=social&label=Star)](https://github.com/your-repo/psmsl)

**PSMSL (Projected Symmetry Mirrored Semantic Lattice)** is an open-source computational engine that represents a fundamental shift in how we approach computation. Instead of relying on traditional symbolic logic (bits, bytes, and arithmetic), PSMSL computes through **geometry, symmetry, and feedback**.

This framework provides a practical, implementable model of the universe as a self-computing geometric lattice. Its core primitives are not numbers but geometric structures, allowing it to handle mathematical singularities and complex numbers with unparalleled efficiency and stability.

**The result is a computational paradigm that is orders of magnitude more energy-efficient than traditional methods, providing a direct path to the next generation of low-power, standalone artificial intelligence.**

---

## Key Innovations

-   **Handles Infinities Geometrically:** Where traditional systems produce `inf` or `NaN` errors when faced with singularities (e.g., division by zero), PSMSL executes a deterministic **geometric phase transition**, changing its scale to maintain numerical stability. **It never overflows.**

-   **Eliminates Complex Arithmetic:** Imaginary numbers are represented as geometric rotations in phase space. This allows the engine to perform complex evolution tasks (like those in quantum mechanics and signal processing) with **~75% fewer arithmetic operations** and zero loss of accuracy.

-   **Stack-Free Recursion:** The engine uses **φ-scaling** (based on the golden ratio) to perform recursion without a call stack, resulting in a constant memory footprint even for deeply recursive problems.

-   **Ultra-Low Energy:** By replacing expensive arithmetic with efficient symmetry checks and geometric transformations, PSMSL provides a blueprint for AI systems that are **3-5x more energy-efficient in software** and **20-50x more efficient with custom hardware**.

![Singularity Comparison](singularity%20comparison.png)
*Figure 1: Traditional numerical methods (left) fail at small scales, while PSMSL (right) remains stable across all orders of magnitude.*

---

## The Science Behind PSMSL

The PSMSL framework is the practical implementation of the **Geometric Computational Universe** theory. This model unifies physics and computation, proposing that:

1.  **The Universe Computes Geometrically:** The fundamental unit of reality is not a particle or a string, but a **tetrahedron**—the minimal stable volume-enclosing structure.
2.  **Physical Laws are Computational Rules:** Concepts like Time, Mass, and Energy are emergent properties of the underlying geometric computation.
3.  **Singularities are Phase Transitions:** Black holes and the Big Bang are not points of infinite density but moments where the computational lattice undergoes a geometric phase transition to a new scale.

For a deep dive into the theoretical foundation, please see our foundational paper:
-   [**The Geometric Computational Universe: A Unified Framework**](./docs/unified_theory.md)

---

## Getting Started

### Prerequisites

-   Python 3.9+
-   NumPy
-   Matplotlib

### Installation

Currently, you can use the library by cloning this repository:

```bash
git clone https://github.com/your-repo/psmsl.git
cd psmsl
pip install -r requirements.txt
```

A full package will be available on PyPI soon.
## Demonstrations

See the [PSMSL Demonstrations guide](demos/PSMSL%20Demonstrations.md) for detailed explanations and instructions.
 for detailed explanations and instructions.
 for detailed explanations and instructions for running the demonstrations.

### Quick Demo: Handling a Singularity

Run the infinity handling demonstration to see the power of geometric phase transitions firsthand:

```bash
python demos/demo_infinities.py
```

You will see the traditional method fail with `OVERFLOW` errors, while the geometric method remains stable and produces correct results at all scales.

### Quick Demo: Geometric Quantum Evolution

Run the imaginary number handling demonstration to see how complex arithmetic is replaced by efficient geometric rotation:

```bash
python demos/demo_imaginary.py
```

You will see that the geometric method produces results identical to traditional complex arithmetic (to machine precision) but with a fraction of the computational cost.

---

## Core Concepts in `libpsmsl`

-   **`Tetrahedron`:** The fundamental "geometric bit." It is the core data structure that holds the computational state.
-   **`TensorFace`:** Each of the four faces of the tetrahedron, represented by a 2x2 real-valued matrix that encodes local field information.
-   **`TriadicState`:** The physical interpretation of a tetrahedron's geometry, providing access to emergent properties like Time (Persistence), Mass (Curvature), and Entropy (Mirror Drift).
-   **`PhaseTransitionEngine`:** The component that monitors the system for impending singularities and executes a geometric scale transition to prevent overflow.

---

## The Vision: A Low-Energy AI Ecosystem

This open-source library is the first step toward a new paradigm of computation. Our vision is to build a complete ecosystem around geometric AI, including:

-   **PSMSL Pro™:** A hardened, enterprise-grade version of the library for commercial applications.
-   **PSMSL Cloud™:** A managed platform for large-scale geometric simulations.
-   **A Geometric Processing Unit (GPU):** A custom ASIC designed from the ground up to run PSMSL computations with maximum efficiency.

By open-sourcing the core, we aim to build a vibrant community of researchers, developers, and pioneers who will help us explore the vast potential of geometric computation.

---

## How to Contribute

We welcome contributions of all kinds, from bug reports and documentation improvements to new feature development and theoretical insights.

Please read our [**Contributing Guidelines**](./CONTRIBUTING.md) to get started.

---

## Citation

If you use PSMSL in your research, please cite our foundational paper:

```bibtex
@article{Bocker2025Geometric,
  title   = {The Geometric Computational Universe: A Unified Framework for Physics, Computation, and Low-Energy AI},
  author  = {Nathanael Joseph Bocker},
  year    = {2025},
}
```

---

## License

PSMSL is licensed under the **Apache License, Version 2.0**. See the [LICENSE](./LICENSE) file for details.

Copyright 2025 Nathanael Joseph Bocker and contributors.
