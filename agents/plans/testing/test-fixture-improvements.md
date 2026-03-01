# Test Fixture Improvements Plan

## Overview

Many tests in the Stanza project use `tempfile.TemporaryDirectory()` or `tempfile.NamedTemporaryFile()` directly in test functions, which can lead to:
- Path separator issues on Windows (when combined with TEST_WORKING_DIR)
- Inconsistent cleanup behavior
- Verbose test code with repeated patterns
- Side effects between tests if cleanup fails
- Difficult-to-maintain test code

This plan outlines improvements to standardize on pytest fixtures for better test isolation and maintainability.

## Benefits of Using Pytest Fixtures

1. **Automatic cleanup** - pytest's `tmp_path` and `tmp_path_factory` fixtures automatically clean up after tests
2. **Better isolation** - Each test gets a fresh temporary directory
3. **Cross-platform compatibility** - `Path` objects handle platform differences
4. **Reusability** - Fixtures can be shared across tests and test classes
5. **Clarity** - Test intent is clearer without boilerplate setup/teardown code
6. **Scope control** - Session, module, class, or function-scoped fixtures

## Current State Analysis

### Files Using tempfile.TemporaryDirectory

```
stanza/tests/common/
  - test_foundation_cache.py: 1 occurrence
  - test_pretrain.py: 4 occurrences (some skipped)
  - test_utils.py: 6 occurrences
  - test_data_conversion.py: 2 occurrences
  - test_char_model.py: 3+ occurrences (in class)

stanza/tests/ner/
  - test_suc3.py: 2 occurrences

stanza/tests/tokenization/
  - test_tokenize_data.py: 2 occurrences
  - test_tokenization_orchid.py: 1 occurrence
  - test_tokenization_lst20.py: 1 occurrence

stanza/tests/constituency/
  - test_vietnamese.py: 1 occurrence
  - test_trainer.py: Multiple occurrences
```

### Files Using tempfile.NamedTemporaryFile

```
stanza/tests/common/
  - test_pretrain.py: 2 occurrences (in skipped tests)

stanza/tests/tokenization/
  - test_tokenize_data.py: 2 occurrences
```

### Files Already Using tmp_path (Good Examples)

```
stanza/tests/ner/
  - test_ner_training.py: Excellent use of tmp_path fixture

stanza/tests/depparse/
  - test_parser.py: Good use of tmp_path fixture

stanza/tests/pos/
  - test_tagger.py: Uses tmp_path fixture

stanza/tests/constituency/
  - test_convert_arboretum.py: Recently updated to use fixtures
```

## Improvement Categories

### Category 1: Simple Replacement (High Priority)

These tests use `tempfile.TemporaryDirectory()` in a straightforward way and can be easily converted to `tmp_path`.

#### Files:
- `stanza/tests/ner/test_suc3.py`
  - `test_read_zip()`: Direct replacement with `tmp_path`
  - `test_read_raw()`: Direct replacement with `tmp_path`
  
- `stanza/tests/common/test_data_conversion.py`
  - `test_file()`: Direct replacement with `tmp_path`
  - `test_zip_file()`: Direct replacement with `tmp_path`

- `stanza/tests/tokenization/test_tokenization_orchid.py`
  - `test_orchid()`: Direct replacement with `tmp_path`

- `stanza/tests/tokenization/test_tokenization_lst20.py`
  - `test_lst20()`: Direct replacement with `tmp_path`

#### Pattern:
```python
# Before
def test_something():
    with tempfile.TemporaryDirectory() as tempdir:
        file_path = Path(tempdir) / "file.txt"
        # ... test code ...

# After
def test_something(tmp_path):
    file_path = tmp_path / "file.txt"
    # ... test code ...
```

### Category 2: Class-Based Tests (Medium Priority)

These tests are in test classes and would benefit from class or module-scoped fixtures.

#### Files:
- `stanza/tests/common/test_char_model.py`
  - Class: `TestCharModel`
  - Multiple methods use `tempfile.TemporaryDirectory()`
  - Could use class-scoped or function-scoped `tmp_path` depending on test independence

#### Pattern:
```python
# Before
class TestCharModel:
    def test_single_file_vocab(self):
        with tempfile.TemporaryDirectory() as tempdir:
            # ... test code ...

# After - Option 1: Function-scoped (if tests are independent)
class TestCharModel:
    def test_single_file_vocab(self, tmp_path):
        # ... test code ...

# After - Option 2: Class-scoped (if setup can be shared)
class TestCharModel:
    @pytest.fixture(scope="class")
    def test_dir(self, tmp_path_factory):
        return tmp_path_factory.mktemp("char_model")
    
    def test_single_file_vocab(self, test_dir):
        # ... test code ...
```

### Category 3: Reusable Fixtures (Medium Priority)

These tests create common test data and could benefit from shared fixtures.

#### Files:
- `stanza/tests/tokenization/test_tokenize_data.py`
  - Has helper function `write_tokenizer_input()` that uses NamedTemporaryFile
  - Could create a fixture that returns a function factory
  - Currently uses `TEST_WORKING_DIR` which causes path issues

#### Pattern:
```python
# Before
def write_tokenizer_input(test_dir, raw_text, labels):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=test_dir, delete=False) as fout:
        txt_file = fout.name
        fout.write(raw_text)
    # ...
    return txt_file, label_file

def test_has_mwt():
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        txt_file, label_file = write_tokenizer_input(test_dir, NO_MWT_TEXT, NO_MWT_LABELS)
        # ...

# After
@pytest.fixture
def tokenizer_input_writer(tmp_path):
    def write(raw_text, labels):
        txt_file = tmp_path / "input.txt"
        label_file = tmp_path / "labels.txt"
        txt_file.write_text(raw_text, encoding="utf-8")
        label_file.write_text(labels, encoding="utf-8")
        return str(txt_file), str(label_file)
    return write

def test_has_mwt(tokenizer_input_writer):
    txt_file, label_file = tokenizer_input_writer(NO_MWT_TEXT, NO_MWT_LABELS)
    data = DataLoader(args=FAKE_PROPERTIES, input_files={'txt': txt_file, 'label': label_file})
    assert not data.has_mwt()
```

### Category 4: TEST_WORKING_DIR Usage (High Priority - Windows Compatibility)

These tests combine `tempfile.TemporaryDirectory()` with `TEST_WORKING_DIR`, which caused path separator issues on Windows.

#### Files:
- `stanza/tests/common/test_utils.py`
  - All 6 occurrences use `dir=str(TEST_WORKING_DIR / 'out')`
  - Should use `tmp_path` instead

- `stanza/tests/tokenization/test_tokenize_data.py`
  - Uses `dir=TEST_WORKING_DIR`
  - Should use `tmp_path` instead

- `stanza/tests/common/test_pretrain.py`
  - Some skipped tests use `dir=TEST_WORKING_DIR`
  - Should use `tmp_path` when tests are re-enabled

#### Issue:
Using `dir=TEST_WORKING_DIR` creates paths like:
`C:\Users\...\Cache\1.11.0/out/tmp123` (mixed separators on Windows)

#### Solution:
Simply use `tmp_path` which pytest manages and cleans up automatically.

### Category 5: NamedTemporaryFile Usage (Low Priority)

These tests use `tempfile.NamedTemporaryFile` with `delete=False` and manual cleanup.

#### Files:
- `stanza/tests/common/test_pretrain.py` (skipped tests)
  - `test_resave_pretrain()`: Uses NamedTemporaryFile with manual `unlink()`
  - `test_whitespace()`: Uses NamedTemporaryFile with manual `unlink()`

- `stanza/tests/tokenization/test_tokenize_data.py`
  - `write_tokenizer_input()`: Uses NamedTemporaryFile with `delete=False`

#### Pattern:
```python
# Before
def test_something():
    test_file = tempfile.NamedTemporaryFile(dir=str(TEST_WORKING_DIR / 'out'), suffix=".pt", delete=False)
    try:
        test_file.close()
        # ... use test_file.name ...
    finally:
        Path(test_file.name).unlink()

# After
def test_something(tmp_path):
    test_file = tmp_path / "test.pt"
    # ... use test_file ...
    # Automatic cleanup by pytest
```

### Category 6: Special Cases (Low Priority)

#### Files:
- `stanza/tests/common/test_foundation_cache.py`
  - Uses `tempfile.TemporaryDirectory(dir=".")`
  - Tests cache foundation specifically in current directory
  - May need to keep current approach or use `tmp_path` with different logic

- `stanza/tests/constituency/test_vietnamese.py`
  - Creates pretrain files in temp directory
  - Could benefit from a `vietnamese_pretrain` fixture

## Implementation Plan

### Phase 1: Quick Wins (Week 1)
- Convert all Category 1 files (simple replacements)
- Fix all Category 4 files (TEST_WORKING_DIR issues for Windows compatibility)
- Files to update:
  - `stanza/tests/ner/test_suc3.py`
  - `stanza/tests/common/test_data_conversion.py`
  - `stanza/tests/common/test_utils.py`
  - `stanza/tests/tokenization/test_tokenization_orchid.py`
  - `stanza/tests/tokenization/test_tokenization_lst20.py`

### Phase 2: Test Classes (Week 2)
- Convert all Category 2 files (class-based tests)
- Files to update:
  - `stanza/tests/common/test_char_model.py`

### Phase 3: Shared Fixtures (Week 3)
- Create reusable fixtures for Category 3 files
- Files to update:
  - `stanza/tests/tokenization/test_tokenize_data.py`
  - `stanza/tests/constituency/test_vietnamese.py`

### Phase 4: Review and Special Cases (Week 4)
- Review Category 5 and 6 files
- Update or document any special cases
- Create shared conftest.py fixtures if patterns emerge

## Testing Strategy

For each file updated:
1. Run the specific test file before changes
2. Make the fixture conversion
3. Run the test file after changes
4. Verify tests still pass and behavior is unchanged
5. Check that temporary files are properly cleaned up
6. Test on both Windows and Linux if possible

## Validation Checklist

For each converted test:
- [ ] Test passes with same behavior as before
- [ ] No manual cleanup code (try/finally, unlink, etc.)
- [ ] Uses pytest fixtures (`tmp_path` or `tmp_path_factory`)
- [ ] No mixed path separators on Windows
- [ ] Temporary files are automatically cleaned up
- [ ] Test is more concise and readable
- [ ] No references to `TEST_WORKING_DIR` for temp file creation

## Common Patterns Reference

### Pattern 1: Basic File Creation
```python
def test_example(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding="utf-8")
    # ... test code ...
```

### Pattern 2: Subdirectories
```python
def test_example(tmp_path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file = subdir / "test.txt"
    test_file.write_text("content", encoding="utf-8")
    # ... test code ...
```

### Pattern 3: Multiple Files
```python
def test_example(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("content1", encoding="utf-8")
    file2.write_text("content2", encoding="utf-8")
    # ... test code ...
```

### Pattern 4: Reusable Fixture
```python
@pytest.fixture
def sample_data_dir(tmp_path):
    """Create a directory with sample test data"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "file1.txt").write_text("data1", encoding="utf-8")
    (data_dir / "file2.txt").write_text("data2", encoding="utf-8")
    return data_dir

def test_example(sample_data_dir):
    files = list(sample_data_dir.glob("*.txt"))
    assert len(files) == 2
```

### Pattern 5: Class-Scoped Fixture
```python
class TestSuite:
    @pytest.fixture(scope="class")
    def shared_dir(self, tmp_path_factory):
        """Shared temp directory for all tests in class"""
        return tmp_path_factory.mktemp("shared")
    
    def test_one(self, shared_dir):
        # ... test code ...
    
    def test_two(self, shared_dir):
        # ... test code ...
```

## Benefits Summary

After completing this plan:
1. All tests will use pytest's standard temporary directory fixtures
2. No more Windows path separator issues
3. Guaranteed cleanup - no leftover temp files
4. More concise and readable test code
5. Better test isolation
6. Consistent patterns across the test suite
7. Easier to maintain and extend tests

## Notes

- Priority is on Windows compatibility issues (Category 4)
- Simple replacements (Category 1) provide quick value
- Some tests may have legitimate reasons to use specific temp directory locations
- Document any exceptions or special cases
- Consider creating a testing best practices guide after completion
