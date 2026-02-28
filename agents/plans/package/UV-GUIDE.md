# UV Package Manager Guide for Stanza

This guide helps you use `uv` - a fast, modern Python package manager - for developing Stanza.

## What is UV?

uv is an extremely fast Python package installer and resolver, written in Rust. It can be 5-10x faster than pip while providing the same interface and reliability.

- Official Repository: https://github.com/astral-sh/uv
- Documentation: https://github.com/astral-sh/uv#readme
- Installation: https://github.com/astral-sh/uv?tab=readme-ov-file#installation

## Quick Start

### 1. Install UV

#### On macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### On Windows (PowerShell):
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Verify Installation:
```bash
uv --version
```

### 2. Install Stanza Development Environment

```bash
# Navigate to Stanza directory
cd c:\projects\nlp\stanza

# Install core and test dependencies
uv pip install -e ".[dev,test,transformers,tokenizers]"

# Or install everything
uv pip install -e ".[all]"
```

### 3. Verify Installation

```bash
# Check installed packages
uv pip list

# Verify Stanza is installed
uv run python -c "import stanza; print(stanza.__version__)"
```

## Common Commands

### Package Management

```bash
# Install packages
uv pip install package_name
uv pip install package_name==1.0.0    # Specific version
uv pip install package_name>=1.0.0    # Minimum version

# Install editable (development) mode
uv pip install -e .

# Install with optional dependencies
uv pip install -e ".[dev,test]"

# List installed packages
uv pip list
uv pip list | grep numpy

# Show package information
uv pip show numpy

# Uninstall packages
uv pip uninstall package_name -y
```

### Code Quality Tools

```bash
# Run Ruff (linting)
uv run ruff check .
uv run ruff check . --fix          # Auto-fix issues
uv run ruff format .               # Format code

# Run MyPy (type checking)
uv run mypy stanza --ignore-missing-imports

# Run Tests
uv run pytest stanza/tests -v
uv run pytest stanza/tests -v -k test_name  # Run specific test

# Run specific test file
uv run pytest stanza/tests/common/test_doc.py -v

# Check coverage
uv run pytest stanza/tests --cov=stanza --cov-report=html
```

## Development Workflow

### Setting Up Development Environment

```bash
# Clone and enter the repository
git clone https://github.com/stanfordnlp/stanza.git
cd stanza

# Install all development tools
uv pip install -e ".[all]"
```

### Making Code Changes

```bash
# 1. Create a new branch
git checkout -b feature/your-feature-name

# 2. Make code changes
# Edit files in your editor

# 3. Check code quality
uv run ruff check stanza --fix    # Auto-fix linting issues
uv run ruff format stanza          # Format code
uv run mypy stanza --ignore-missing-imports  # Type check

# 4. Run tests
uv run pytest stanza/tests -v

# 5. Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

### Local Testing

```bash
# Run all tests
uv run pytest stanza/tests

# Run specific test module
uv run pytest stanza/tests/common/test_doc.py

# Run tests matching pattern
uv run pytest stanza/tests -k "tokenize"

# Run with verbose output
uv run pytest stanza/tests -vv

# Run with coverage
uv run pytest stanza/tests --cov=stanza

# Run specific test and show print statements
uv run pytest stanza/tests/common/test_doc.py -s
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/uv-build-checks.yaml`) runs:

1. Matrix Testing: Python 3.9-3.13 on Ubuntu, Windows, macOS
2. Ruff Format Check: Ensures consistent code style
3. Ruff Linting: Checks for errors and warnings
4. MyPy Type Checking: Validates type hints
5. Pytest Unit Tests: Runs full test suite
6. Coverage Report: Uploads to Codecov

### Local Simulation of CI

```bash
# Run what CI runs (using uv)
uv pip install -e ".[dev,test,transformers,tokenizers]"
uv run ruff check . --diff
uv run ruff check . --select=E,W,F
uv run mypy stanza --ignore-missing-imports --no-error-summary
uv run pytest stanza/tests -v --tb=short --timeout=300
```

## Comparison: pip vs uv

| Feature | pip | uv |
|---------|-----|-----|
| Speed | Baseline | 5-10x faster |
| Resolution | Sequential | Parallel |
| Lock files | External tools | Built-in (future) |
| Reproducibility | Variable | Excellent |
| Python API | Yes | Partial |
| Backwards compatible | Yes | Yes ✅ |

## Performance Tips

### 1. Use UV Cache
```bash
# Cache is automatically stored in:
# - Linux/macOS: ~/.cache/uv
# - Windows: %LOCALAPPDATA%\uv\cache

# Clear cache if needed
rm -rf ~/.cache/uv/  # or delete Windows equivalent
```

### 2. Parallel Installation
UV automatically uses parallelism - no special flags needed!

### 3. Shallow Clones
```bash
# For Git dependencies, clone with depth
git clone --depth=1 https://github.com/repo.git
```

## Troubleshooting

### Issue: "uv command not found"
```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env  # Add to PATH
```

### Issue: "Failed to find interpreter"
```bash
# Ensure Python 3.9+ is installed
python --version

# Specify Python explicitly
uv pip install --python 3.11 package_name
```

### Issue: GPU/CUDA Support with PyTorch
```bash
# For CUDA 11.8
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CPU only
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Module Import Errors
```bash
# Reinstall in editable mode
uv pip install -e .

# Verify installation
uv run python -c "import stanza; print(stanza.__file__)"
```

## Configuration Files

### pyproject.toml
Located at repository root. Defines:
- Package metadata and dependencies
- Tool configurations (ruff, mypy, pytest, black)
- Optional dependency groups
- Python version requirements

### .github/dependabot.yml
Automated dependency updates:
- pip ecosystem (weekly)
- github-actions (weekly)
- uv ecosystem (weekly)

### .github/workflows/uv-build-checks.yaml
CI/CD pipeline with:
- Matrix testing (3 OS × 5 Python versions)
- Code quality checks
- Type validation
- Test execution

## Advanced Usage

### Virtual Environment Management
```bash
# UV manages environments automatically, or explicitly:
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Sync Dependencies (Lock File - Future)
```bash
# When UV adds lock file support
uv sync        # Install from locked file
uv export ...  # Export lock file
```

### Check for Outdated Packages
```bash
# Using pip list
uv pip list --outdated
```

## Additional Resources

- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [Stanza Documentation](https://stanfordnlp.github.io/stanza/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PyTorch Installation](https://pytorch.org/get-started/locally/)

## Getting Help

### Report Issues
- [Stanza Issues](https://github.com/stanfordnlp/stanza/issues)
- [uv Issues](https://github.com/astral-sh/uv/issues)

### Documentation
- Run `uv --help` for general help
- Run `uv pip --help` for pip-specific help
- See [pyproject.toml](pyproject.toml) for package configuration

---

Last Updated: February 28, 2026  
UV Version: Latest  
Python Versions Supported: 3.9+
