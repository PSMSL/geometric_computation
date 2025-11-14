# PSMSL Project Structure

This document describes the organization of the PSMSL open-source project.

## Directory Structure

```
psmsl-project/
│
├── LICENSE                    # Apache 2.0 license
├── README.md                  # Main project README
├── CONTRIBUTING.md            # Contribution guidelines
├── CODE_OF_CONDUCT.md         # Community code of conduct
├── setup.py                   # Package installation script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
│
├── libpsmsl/                  # Core library (open-source)
│   ├── __init__.py           # Package initialization
│   └── psmsl_core.py         # Core geometric primitives
│
├── demos/                     # Demonstration scripts
│   ├── demo_infinities.py    # Singularity handling demo
│   └── demo_imaginary.py     # Complex number handling demo
│
├── docs/                      # Documentation
│   ├── unified_theory.md     # Theoretical foundation
│   ├── architectural_requirements.md  # Technical specifications
│   └── demonstration_results.md       # Validation results
│
├── tests/                     # Unit and integration tests
│   └── (to be populated)
│
└── examples/                  # Example applications
    └── (to be populated)
```

## Core Components

### Open-Source Core (`libpsmsl/`)

This is the heart of the project, licensed under Apache 2.0. It includes:

-   **Geometric Primitives:** `TensorFace`, `Tetrahedron`, `TriadicState`
-   **Computational Engines:** `PhaseTransitionDetector`, `PhaseTransitionEngine`
-   **Utility Functions:** `handle_imaginary_via_rotation`, constants like `PHI`

### Demonstrations (`demos/`)

Executable scripts that showcase the capabilities of the framework:

-   **Infinity Handling:** Shows how geometric phase transitions prevent numerical overflow
-   **Imaginary Number Handling:** Demonstrates geometric rotation as a replacement for complex arithmetic

### Documentation (`docs/`)

Comprehensive documentation including:

-   Theoretical foundations and physics background
-   Technical architecture and design decisions
-   Validation results and performance benchmarks

## Future Additions

As the project grows, we will add:

-   **`tests/`:** Comprehensive test suite using pytest
-   **`examples/`:** Real-world application examples (quantum chemistry, signal processing, etc.)
-   **`benchmarks/`:** Performance comparison scripts
-   **`hardware/`:** HDL code for FPGA implementations (separate repository)

## Commercial Extensions (Not in This Repository)

The following commercial products are built on top of this open-source core but are maintained in separate, proprietary repositories:

-   **PSMSL Pro™:** Enterprise-grade optimized library (C++/Rust)
-   **PSMSL Cloud™:** Managed computational platform
-   **PSMSL Accelerate™:** Hardware-specific implementations (GPU, FPGA, ASIC)

This separation allows us to maintain a thriving open-source community while generating revenue to fund continued development.
