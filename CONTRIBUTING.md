# Contributing to PSMSL

First off, thank you for considering contributing to PSMSL! It's people like you that make the open-source community such a great place. We welcome contributions of all kinds, from fixing typos to implementing new features.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [your-email@example.com].

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/your-repo/psmsl/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/your-repo/psmsl/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

- Open a new issue and provide a clear description of the enhancement you are suggesting.
- Explain why this enhancement would be useful to other PSMSL users.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue that pull request!

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issues and pull requests liberally after the first line.

### Python Styleguide

All Python must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/), with the exception of line length (we use 88 characters, like Black).

We use `black` and `flake8` to enforce style. Please run them on your code before submitting a pull request.

```bash
pip install black flake8
black .
flake8 .
```

## Thank You!

Your contributions will help shape the future of computing. We are excited to see what you build with us.
