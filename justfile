# Justfile for Stanza development tasks
# Install just: cargo install just OR pip install rust-just
# Run 'just --list' to see all available commands

# Default recipe to display help
default:
    @just --list

# Install package in development mode
install:
    uv pip install -e .

# Install with all optional dependencies
install-all:
    uv pip install -e ".[all]"

# Install with specific dependency groups
install-dev:
    uv pip install -e ".[dev,test,lint]"

# Install test dependencies only
install-test:
    uv pip install -e ".[test]"

# Install with transformers support
install-transformers:
    uv pip install -e ".[transformers]"

# Install with morphseg support
install-morphseg:
    uv pip install -e ".[morphseg]"

# Run all tests
test:
    uv run pytest stanza/tests/

# Run tests marked for Travis CI
test-travis:
    uv run pytest -m travis stanza/tests/

# Run tests excluding optional dependencies
test-core:
    uv run pytest -m "not transformers and not morphseg" stanza/tests/

# Run transformer-related tests
test-transformers:
    uv run pytest -m transformers stanza/tests/

# Run morphseg-related tests
test-morphseg:
    uv run pytest -m morphseg stanza/tests/

# Run specific test file
test-file FILE:
    uv run pytest {{FILE}}

# Run tests with coverage report
test-coverage:
    uv run pytest --cov=stanza --cov-report=html --cov-report=term stanza/tests/

# Run tests in verbose mode
test-verbose:
    uv run pytest -v stanza/tests/

# Run linter checks
lint:
    uv run ruff check .

# Run linter and auto-fix issues
lint-fix:
    uv run ruff check --fix .

# Format code with ruff
format:
    uv run ruff format .

# Check formatting without making changes
format-check:
    uv run ruff format --check .

# Run ruff summary script (Windows)
lint-summary:
    pwsh scripts/ruff-summary.ps1

# Run line length check (Windows)
check-line-length:
    pwsh scripts/line-length.ps1

# Run all checks (lint + format check + tests)
check: lint format-check test-core

# Clean build artifacts
clean:
    rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov/
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Clean cache and temporary test files
clean-cache:
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Build distribution packages
build:
    uv build

# Download word vectors (Windows)
download-vectors-win:
    pwsh scripts/download_vectors.ps1

# Download word vectors (Unix)
download-vectors:
    bash scripts/download_vectors.sh

# Run Python REPL with stanza imported
repl:
    uv run python -c "import stanza; import code; code.interact(local=dict(globals(), **locals()))"

# Show project info
info:
    @echo "Stanza NLP Library"
    @echo "Python version: $(python --version)"
    @echo "Pip version: $(pip --version)"
    @echo "Installed packages:"
    @pip list | grep -E "(stanza|torch|transformers|pytest|ruff)"

# Update dependencies
update-deps:
    # pip install --upgrade pip setuptools wheel
    pip install --upgrade -e ".[dev,test,lint]"

# Run type checking with mypy
typecheck-mypy:
    mypy stanza/

# Run type checking with ty
typecheck:
    ty check stanza/

# Run specific test class
test-class CLASS:
    uv run pytest stanza/tests/ -k {{CLASS}}

# Run tests matching a pattern
test-pattern PATTERN:
    uv run pytest stanza/tests/ -k {{PATTERN}}

# Run slow tests
test-slow:
    uv run pytest -m slow stanza/tests/

# Run GPU tests
test-gpu:
    uv run pytest -m gpu stanza/tests/

# Run client tests
test-client:
    uv run pytest -m client stanza/tests/

# Run pipeline tests
test-pipeline:
    uv run pytest -m pipeline stanza/tests/

# Show test markers
test-markers:
    uv run pytest --markers

# Install pre-commit hooks (if using pre-commit)
setup-hooks-pre:
    uv pip install pre-commit
    pre-commit install

# Install pre-commit hooks
setup-hooks:
    uv pip install prek
    prek install

# Run pre-commit on all files
prek:
    prek run --all-files

# Run pre-commit on all files
pre-commit:
    pre-commit run --all-files

# Generate test coverage report and open in browser
coverage-html: test-coverage
    uv run python -m webbrowser htmlcov/index.html

# Validate pyproject.toml
validate-config:
    uv run python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"

# Count lines of code
count-loc:
    find stanza -name "*.py" -not -path "*/tests/*" | xargs wc -l | tail -1

# Search for TODO comments
todos:
    grep -r "TODO" stanza/ --include="*.py" || echo "No TODOs found"

# Search for FIXME comments
fixmes:
    grep -r "FIXME" stanza/ --include="*.py" || echo "No FIXMEs found"

# Quick development loop: format, lint-fix, test core
dev: format lint-fix test-core
    @echo "✓ Development checks passed!"
