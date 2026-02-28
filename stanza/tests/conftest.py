"""
Shared pytest fixtures and configuration for stanza tests

This module provides pytest plugins config and shared fixtures for all tests.

Markers:
    train: Tests that train models (slow, skipped by default)
    slow: Tests that are slow to run
    gpu: Tests that require GPU
    integration: Integration tests across multiple components
    benchmark: Performance benchmark tests
"""

import logging

import pytest


# Module availability checks
def _check_transformers_available():
    """Check if transformers library is available."""
    try:
        import transformers
        return True
    except ImportError:
        return False


def _check_morphseg_available():
    """Check if morphseg library is available."""
    try:
        import morphseg
        return True
    except ImportError:
        return False


TRANSFORMERS_AVAILABLE = _check_transformers_available()
MORPHSEG_AVAILABLE = _check_morphseg_available()

# Make pytest skip condition available for imports
requires_transformers = pytest.mark.skipif(
    not TRANSFORMERS_AVAILABLE,
    reason="transformers library not installed",
)

requires_morphseg = pytest.mark.skipif(
    not MORPHSEG_AVAILABLE,
    reason="morphseg library not installed",
)


def pytest_configure(config):
    """Configure pytest with custom markers and logging."""
    # Define custom markers
    config.addinivalue_line(
        "markers",
        "train: mark test as a training test (slow, skipped by default)",
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running",
    )
    config.addinivalue_line(
        "markers",
        "gpu: mark test as requiring GPU",
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test",
    )
    config.addinivalue_line(
        "markers",
        "benchmark: mark test for performance benchmarking",
    )

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically apply skip conditions based on markers.
    This hook runs after test collection and modifies test items.
    
    By default, skips:
    - train: Model training tests (slow, run with -m train)
    - Tests requiring unavailable libraries (transformers, morphseg)
    """
    skip_transformers = pytest.mark.skip(reason="transformers library not installed")
    skip_morphseg = pytest.mark.skip(reason="morphseg library not installed")
    skip_train = pytest.mark.skip(
        reason="Training tests skipped by default (slow). Use -m train to run them.",
    )

    # Check if user explicitly requested training tests
    train_marker = config.getoption("-m", default="")
    run_training = "train" in train_marker if train_marker else False

    for item in items:
        # Skip training tests unless explicitly requested
        if "train" in item.keywords and not run_training:
            item.add_marker(skip_train)

        # Skip tests marked with @pytest.mark.transformers if transformers not available
        if "transformers" in item.keywords and not TRANSFORMERS_AVAILABLE:
            item.add_marker(skip_transformers)

        # Skip tests marked with @pytest.mark.morphseg if morphseg not available
        if "morphseg" in item.keywords and not MORPHSEG_AVAILABLE:
            item.add_marker(skip_morphseg)
