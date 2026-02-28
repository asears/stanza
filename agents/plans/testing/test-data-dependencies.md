# Test Data Dependencies - Architectural Issues and Solutions

## Problem Statement

Tests are failing during collection (import time) due to module-level file operations that attempt to load test data before the test environment is properly initialized. This violates pytest best practices and causes:

1. Import-time failures: Files opened during module import fail if paths don't exist
2. Non-deterministic test discovery: Tests can't be collected without file dependencies
3. Environment dependencies: Tests assume specific directory structures exist
4. Hard to debug: Failures occur before test execution, making debugging difficult

### Example Issue

```python
# stanza/tests/server/test_server_request.py:150
# This fails during import if file doesn't exist
FRENCH_JSON_GOLD = json.loads(open(f'{TEST_WORKING_DIR}/out/example_french.json', encoding="utf-8").read())
```

## Root Causes

1. Module-level file I/O: Data loading happens at import time, not test time
2. Incorrect path assumptions: Using `TEST_WORKING_DIR` instead of test data directory
3. Missing fixtures: No pytest fixtures for loading test data
4. Hardcoded paths: Paths embedded in test code instead of configuration

## Proposed Solutions

### Solution 1: Pytest Fixtures (Recommended)

Convert module-level data loading to pytest fixtures:

```python
import pytest
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / 'data'

@pytest.fixture(scope='module')
def french_json_gold():
    """Load French JSON gold standard data."""
    data_file = TEST_DATA_DIR / 'example_french.json'
    with data_file.open(encoding='utf-8') as f:
        return json.load(f)

def test_annotators_and_output_format(corenlp_client, french_json_gold):
    """Test setting the annotators and output_format"""
    ann = corenlp_client.annotate(FRENCH_DOC, properties=FRENCH_EXTRA_PROPS,
                                  annotators="tokenize,ssplit,mwt,pos", 
                                  output_format="json")
    assert ann == french_json_gold
```

Benefits:
- Lazy loading: Data loaded only when tests run
- Better error handling: pytest captures and reports fixture failures clearly
- Scope control: Can cache at session/module/function level
- Easy to mock or parametrize

### Solution 2: Conftest Shared Fixtures

Create shared fixtures in `conftest.py` for common test data:

```python
# stanza/tests/conftest.py or stanza/tests/server/conftest.py
import pytest
from pathlib import Path

@pytest.fixture(scope='session')
def test_data_dir():
    """Root directory for test data files."""
    return Path(__file__).parent / 'data'

@pytest.fixture(scope='session')
def load_json_fixture(test_data_dir):
    """Factory fixture for loading JSON files."""
    def _load(filename):
        file_path = test_data_dir / filename
        with file_path.open(encoding='utf-8') as f:
            return json.load(f)
    return _load
```

Benefits:
- DRY principle: Reusable across test modules
- Centralized data loading logic
- Easy to extend with caching or validation

### Solution 3: Lazy Module Constants

Use a lazy-loading pattern for module constants:

```python
from functools import lru_cache
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / 'data'

@lru_cache(maxsize=1)
def _load_french_json_gold():
    """Lazy load French JSON gold data."""
    data_file = TEST_DATA_DIR / 'example_french.json'
    with data_file.open(encoding='utf-8') as f:
        return json.load(f)

# Use property or function call in tests
def test_something(corenlp_client):
    french_json_gold = _load_french_json_gold()
    # ... test code
```

Benefits:
- Minimal code changes
- Still allows module-level access pattern
- Data loaded on first use, not import

### Solution 4: Separate Test Data and Working Directories

Clarify the distinction between:
- Test data directory: Static files in `stanza/tests/data/` (committed to git)
- Test working directory: Temporary runtime data in `TEST_WORKING_DIR` (not committed)

```python
from pathlib import Path

# Static test data (committed)
TEST_DATA_DIR = Path(__file__).parent / 'data'

# Runtime working directory (temporary)
from stanza.tests import TEST_WORKING_DIR  # From platformdirs/cache

# Models go in working dir
model_path = Path(TEST_WORKING_DIR) / 'models' / 'en_ewt.pt'

# Gold standard data comes from test data dir
gold_data = TEST_DATA_DIR / 'example_french.json'
```

Benefits:
- Clear separation of concerns
- Prevents mixing static and generated data
- Makes test data requirements explicit

### Solution 5: Resource Management Helpers

Create helper utilities for common patterns:

```python
# stanza/tests/utils.py
from pathlib import Path
import json

def load_test_json(filename, subdir=''):
    """Load JSON from test data directory."""
    data_dir = Path(__file__).parent / 'data'
    if subdir:
        data_dir = data_dir / subdir
    
    file_path = data_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Test data file not found: {file_path}")
    
    with file_path.open(encoding='utf-8') as f:
        return json.load(f)

def load_test_text(filename, subdir=''):
    """Load text from test data directory."""
    data_dir = Path(__file__).parent / 'data'
    if subdir:
        data_dir = data_dir / subdir
    
    file_path = data_dir / filename
    return file_path.read_text(encoding='utf-8')
```

## Implementation Plan

### Priority 1: Fix Import-Time Failures

1. Identify all module-level file operations
2. Convert to fixtures or lazy loading
3. Update affected tests

### Priority 2: Standardize Test Data Access

1. Create `test_data_dir` fixture in root conftest
2. Document the pattern in test documentation
3. Migrate existing tests module by module

### Priority 3: Clean Up Path Handling

1. Separate TEST_DATA_DIR from TEST_WORKING_DIR
2. Use pathlib consistently (see pathlib-migration.md)
3. Remove hardcoded path assumptions

### Priority 4: Improve Test Data Organization

1. Review test data file organization
2. Create subdirectories by component (ner/, pos/, etc.)
3. Add README in test data directory documenting files

## Testing the Migration

1. Run `pytest --collect-only` to ensure all tests can be discovered
2. Run tests with empty `TEST_WORKING_DIR` to verify dependencies
3. Test on clean environment (no cached data)
4. Verify tests work on Windows, Linux, macOS

## Quick Wins

Files with module-level file loading to fix immediately:
- `stanza/tests/server/test_server_request.py` - FRENCH_JSON_GOLD
- Any other modules using `open()` at module level

Search for patterns:
```bash
grep -r "^[A-Z_]* = .*open(" stanza/tests/
grep -r "^[A-Z_]* = .*Path(" stanza/tests/
```

## Long-term Improvements

1. Consider using `pytest-datadir` plugin for test data management
2. Implement test data validation on CI
3. Create test data generation scripts for reproducibility
4. Document test data requirements in CONTRIBUTING.md

## Related Plans

- pathlib-migration.md - Modernizing path handling across tests
- Test data organization and documentation
- CI/CD improvements for test environment setup

## References

- [pytest fixtures documentation](https://docs.pytest.org/en/stable/fixture.html)
- [pytest best practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [lazy loading patterns in python](https://docs.python.org/3/library/functools.html#functools.lru_cache)
