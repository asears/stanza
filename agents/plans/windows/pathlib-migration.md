# Test Suite Pathlib Migration Plan

## Overview

Migrate all test files from using string-based path manipulation (`os.path`) to modern `pathlib.Path` objects for improved readability, cross-platform compatibility, and type safety.

## Progress Log

### 2026-02-28: Batch 1 completed

- Converted path handling in `stanza/tests/setup.py` to `Path` usage for directory creation, joins, and globbing.
- Converted file-read path usage in:
    - `stanza/tests/common/test_foundation_cache.py`
    - `stanza/tests/tokenization/test_tokenization_lst20.py`
    - `stanza/tests/tokenization/test_tokenization_orchid.py`
    - `stanza/tests/tokenization/test_tokenize_files.py`
    - `stanza/tests/tokenization/test_tokenize_utils.py`
- Converted `open()` to `Path.open()` in:
    - `stanza/utils/avg_sent_len.py`
    - `stanza/utils/conll.py`
- Validation: Ruff `PTH` checks pass for all files touched in this batch.
- Remaining work: large `PTH` backlog remains across `stanza/utils/` and multiple test modules.

## Current State

The test suite currently uses a mix of:
- `os.path.join()` for path concatenation
- f-strings with `/` separators (non-portable)
- String-based file operations
- `TEST_WORKING_DIR` as a string constant

## Goals

1. Replace all `os.path` operations with `pathlib.Path`
2. Use `Path` objects throughout for file system operations
3. Maintain backward compatibility during migration
4. Improve test reliability across platforms (Windows, Linux, macOS)

## Migration Strategy

### Phase 1: Foundation (stanza/tests/__init__.py)

Update core test constants to use `pathlib.Path`:

```python
from pathlib import Path
from platformdirs import user_cache_dir

# Convert to Path objects
TEST_WORKING_DIR = Path(os.getenv(TEST_HOME_VAR, user_cache_dir(TEST_DIR_BASE_NAME, 'StanfordNLP', __resources_version__)))
TEST_MODELS_DIR = TEST_WORKING_DIR / 'models'
TEST_CORENLP_DIR = TEST_WORKING_DIR / 'corenlp_dir'
```

### Phase 2: Test Data Access

Create a standard pattern for accessing test data:

```python
# In each test module
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / 'data'

# Usage
data_file = TEST_DATA_DIR / 'example_french.json'
with data_file.open(encoding='utf-8') as f:
    data = json.load(f)
```

### Phase 3: Gradual Migration by Module

Migrate test modules in order of dependency:

1. `stanza/tests/common/` - Foundation classes
2. `stanza/tests/data/` - Data utilities
3. Individual component tests (tokenization, ner, pos, etc.)
4. Pipeline tests
5. Server/client tests

### Phase 4: File Operation Patterns

Replace common patterns:

```python
# Old
file_path = os.path.join(dir_name, 'file.txt')
with open(file_path, 'r') as f:
    content = f.read()

# New
file_path = Path(dir_name) / 'file.txt'
content = file_path.read_text(encoding='utf-8')
```

```python
# Old
if os.path.exists(file_path):
    os.remove(file_path)

# New
if file_path.exists():
    file_path.unlink()
```

```python
# Old
os.makedirs(dir_path, exist_ok=True)

# New
dir_path.mkdir(parents=True, exist_ok=True)
```

## Benefits

1. Cross-platform compatibility: Path separators handled automatically
2. Cleaner code: Path concatenation with `/` operator
3. Type safety: IDE and type checkers can verify Path operations
4. Better error messages: Path objects provide clearer error context
5. Modern Python: Aligns with Python 3.4+ best practices

## Testing Strategy

1. Run full test suite after each module migration
2. Test on Windows, Linux, and macOS
3. Verify no performance regression
4. Ensure backward compatibility with string paths where needed

## Implementation Checklist

- [ ] Update `stanza/tests/__init__.py` constants
- [ ] Create `TEST_DATA_DIR` pattern documentation
- [ ] Migrate `common/` module tests
- [ ] Migrate data utility tests
- [x] Migrate tokenization tests
- [ ] Migrate NER tests
- [ ] Migrate POS tests
- [ ] Migrate dependency parsing tests
- [ ] Migrate lemmatization tests
- [ ] Migrate pipeline tests
- [ ] Migrate server/client tests
- [ ] Migrate constituency parser tests
- [ ] Migrate classifier tests
- [ ] Update documentation
- [ ] Remove deprecated `os.path` usage

## Related Issues

- Module-level file loading should be converted to fixtures (see test-data-dependencies.md)
- Test data organization could be improved alongside this migration

## References

- [pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [PEP 519 - Adding a file system path protocol](https://www.python.org/dev/peps/pep-0519/)
