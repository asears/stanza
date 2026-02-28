# Slow and Integration Tests Strategy

## Overview

Stanza includes slow tests that are integration tests or training-heavy, including model checkpointing, resource loading, and multi-second runtime. This plan addresses identifying, measuring, categorizing, and optimizing these tests.

## Problem Statement

- No distinction between unit tests and integration tests
- Slow tests block CI/CD pipelines (39+ seconds for single tests)
- Training tests are non-deterministic and hard to debug
- No benchmarking infrastructure for performance tracking
- Tests fail intermittently due to resource loading
- Developers don't know which tests are safe to run frequently

## Current Slow Tests

From test runs:
- test_train_pipeline: 39s+ (trains model, loads resources)
- test_train_bert: 30+s (downloads tiny-bert model, trains)
- test_finetune_bert: 40+s (finetuning training)
- test_finetune_bert_layers: 50+s (extended training with checkpoints)
- All constituency training tests: 20-40s each

## Solution: Test Categorization & Benchmarking

### 1. Marker-Based Test Classification

Define pytest markers to categorize test speed:

```python
# pyproject.toml
markers = [
    "unit: fast unit tests (< 1s)",
    "integration: integration tests (1-5s)",
    "slow: slow tests (5-30s)",
    "very_slow: very slow tests (> 30s)",
    "benchmark: performance benchmark tests",
    "training: model training tests",
    "gpu: tests requiring GPU",
]
```

### 2. Mark Existing Slow Tests

```python
@pytest.mark.slow
@pytest.mark.training
def test_train_bert(self, tmp_path, fake_embeddings, train_file, dev_file):
    """Model training test - slow due to transformer loading"""
    pass

@pytest.mark.very_slow
@pytest.mark.integration
@pytest.mark.training
def test_train_pipeline(self, tmp_path, constituency_model):
    """Integration test - trains model and loads in pipeline"""
    pass
```

### 3. Pytest-Benchmark Integration

Use pytest-benchmark for model performance profiling:

```python
import pytest

@pytest.mark.benchmark
def test_inference_performance(benchmark, nlp_pipeline):
    """Benchmark pipeline inference speed"""
    doc = "Barack Obama was born in Hawaii."
    result = benchmark(nlp_pipeline, doc)
    assert result is not None
```

Add pytest-benchmark to pytest config:

```toml
[project.optional-dependencies]
benchmark = [
    "pytest-benchmark>=3.4.0",
]

# pyproject.toml
[tool.pytest.ini_options]
addopts = [
    "--benchmark-disable",  # Disable by default
    "--benchmark-only",     # Run only benchmarks with --benchmark-only
]
```

### 4. Test Duration Tracking

Add pytest-timeout and monitor test durations:

```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-timeout>=2.1",  # Already included
]
```

Configure timeout by test type:

```python
# conftest.py
import pytest

def pytest_configure(config):
    """Add timeout markers based on test type"""
    config.addinivalue_line(
        "markers", "timeout(seconds): set timeout for test"
    )

@pytest.fixture
def timeout(request):
    """Auto-set timeouts based on markers"""
    if request.node.get_closest_marker('very_slow'):
        return 300  # 5 minutes for very slow tests
    elif request.node.get_closest_marker('slow'):
        return 120  # 2 minutes for slow tests
    elif request.node.get_closest_marker('integration'):
        return 30   # 30 seconds for integration tests
    return 10       # 10 seconds for unit tests
```

### 5. Pytest-Eric for Distribution

Use pytest-eric to parallelize test runs across cores:

```bash
# Install pytest-eric (if available)
# pip install pytest-eric

# Run tests in parallel
pytest --eric -n auto stanza/tests/

# Run only fast tests in parallel
pytest --eric -n auto -m "not slow and not very_slow" stanza/tests/
```

Alternative: pytest-xdist (more stable):

```toml
[project.optional-dependencies]
test = [
    "pytest-xdist>=2.5.0",
]
```

```bash
# Parallelize test runs
pytest -n auto stanza/tests/

# Parallelize only fast tests
pytest -n auto -m "not slow" stanza/tests/
```

### 6. Quick Test Subsets for Development

Add justfile recipes for common developer workflows:

```makefile
# justfile - recipes for slow test strategies

# Run only fast unit tests (development)
quick-test:
    pytest -m "not slow and not very_slow" stanza/tests/

# Run integration tests only
test-integration:
    pytest -m "integration" stanza/tests/

# Run all slow tests sequentially
test-slow:
    pytest -m "slow or very_slow" stanza/tests/ --timeout=600

# Run benchmarks with results
benchmark:
    pytest -m benchmark --benchmark-only --benchmark-mean stanza/tests/

# Run training tests with GPU support
test-training-gpu:
    pytest -m "training and gpu" stanza/tests/ --timeout=600

# Continuous integration full suite (can run overnight)
test-full-suite:
    pytest stanza/tests/ --timeout=600 --benchmark-disable
```

### 7. CI/CD Workflow Optimization

```yaml
# .github/workflows/fast-tests.yml
name: Fast Tests
on: [push, pull_request]
jobs:
  fast-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -e ".[dev,test]"
      - run: pytest -m "not slow" --timeout=60

---
# .github/workflows/slow-tests.yml
name: Slow Tests
on:
  schedule:
    - cron: '0 2 * * *'  # Run nightly at 2 AM
concurrency:
  group: slow-tests
jobs:
  slow-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -e ".[dev,test,benchmark]"
      - run: pytest -m "slow or very_slow" --timeout=600
      - run: pytest -m benchmark --benchmark-only --benchmark-compare
```

### 8. Profiling Slow Tests

Create profiling utilities:

```python
# stanza/tests/utils/profiling.py
import cProfile
import pstats
from io import StringIO
import pytest

@pytest.fixture
def profile_test():
    """Profile a test and print top functions"""
    profiler = cProfile.Profile()
    
    def _profile(func):
        profiler.enable()
        result = func()
        profiler.disable()
        
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(10)
        print(s.getvalue())
        
        return result
    
    return _profile
```

Usage in tests:

```python
def test_slow_function_profile(profile_test):
    """Profile slow function"""
    profile_test(lambda: slow_training_function())
```

### 9. Benchmark Comparison Tracking

Store benchmark results in git:

```yaml
# .github/workflows/benchmark-track.yml
- name: Store benchmark results
  if: always()
  run: |
    python -m pytest --benchmark-only \
      --benchmark-json=output.json stanza/tests/
    
    # Compare against baseline
    if [ -f benchmarks/baseline.json ]; then
      python scripts/compare_benchmarks.py \
        benchmarks/baseline.json output.json
    fi
```

## Implementation Roadmap

### Week 1: Marker Infrastructure
- [ ] Add pytest markers to pyproject.toml
- [ ] Create marker documentation
- [ ] Add pytest-timeout configuration

### Week 2: Test Classification
- [ ] Mark all slow tests (30+ tests)
- [ ] Mark all training tests
- [ ] Mark all integration tests

### Week 3: Benchmarking Setup
- [ ] Add pytest-benchmark to dev dependencies
- [ ] Create benchmark test templates
- [ ] Document benchmark practices

### Week 4: CI/CD Updates
- [ ] Create separate fast/slow test workflows
- [ ] Set up nightly benchmark runs
- [ ] Add benchmark comparison reporting

### Week 5: Developer Tooling
- [ ] Add justfile recipes
- [ ] Document test running commands
- [ ] Create pytest plugins for common patterns

## Expected Outcomes

| Metric | Before | After |
|--------|--------|-------|
| Fast test run time | 30+ min | <5 min |
| CI/CD feedback | 1 hour | 5-10 min (fast) |
| Test category clarity | No distinction | 5 categories |
| Performance tracking | Manual | Automated/Tracked |
| Developer experience | Slow feedback | Quick iteration |

## References

### pytest-benchmark
- https://pytest-benchmark.readthedocs.io/
- Storage and comparison: https://pytest-benchmark.readthedocs.io/en/latest/user_guide.html#storage
- JSON format: https://pytest-benchmark.readthedocs.io/en/latest/user_guide.html#json-report

### pytest-xdist (Parallelization)
- https://pytest-xdist.readthedocs.io/
- Load balancing: https://pytest-xdist.readthedocs.io/en/latest/index.html#behavior

### pytest-timeout
- https://pytest-timeout.readthedocs.io/
- Already in dependencies

### Profiling
- cProfile: https://docs.python.org/3/library/profile.html
- scalene: https://github.com/plasma-umass/scalene (GPU-aware)
- py-spy: https://github.com/benfred/py-spy

### Performance Testing
- pytest-performance: https://github.com/pytest-dev/pytest-performance
- airspeed-velocity (asv): https://asv.readthedocs.io/

## Related Plans

- test-cache-cleanup.md: Isolation and resource management
- test-data-dependencies.md: Fixture infrastructure

## Quick Start

```bash
# See all test markers
pytest --markers

# Run only fast tests
just quick-test

# Run specific slow test with profiling
pytest -m training -v --profile stanza/tests/classifiers/test_classifier.py::TestClassifier::test_train_bert

# Compare benchmarks
python scripts/compare_benchmarks.py \
  benchmarks/baseline.json \
  benchmarks/current.json
```
