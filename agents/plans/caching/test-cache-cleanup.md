# Test Cache and Temporary Folder Management

## Problem Statement

Tests are currently generating artifacts in user cache and temp folders, causing:
- ResourceFileNotFoundError when models aren't found in cache
- Security concerns from writing to shared cache directories
- Leftover artifacts accumulating in user temp folders
- Test isolation issues from shared cache state
- Platform-specific path issues (Windows cache paths)

Example error:
```
ResourcesFileNotFoundError: Resources file not found at: 
\AppData\Local\StanfordNLP\stanza_test\Cache\1.11.0/models\resources.json
```

## Root Causes

1. Model Resource Loading: Pipeline initialization attempts to load from default cache locations
2. Checkpoint Saving: Training tests save models to platform-specific temp directories
3. Shared State: Multiple tests may pollute the same cache directory
4. No Cleanup: Temporary artifacts aren't cleaned up after test completion
5. Platform Differences: Windows and Unix cache paths differ

## Solutions

### 1. Isolated Test Artifacts with Fixtures

Create pytest fixtures that provide isolated temp directories per test:

```python
@pytest.fixture
def isolated_cache_dir(tmp_path):
    """Provide isolated cache directory for test"""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir(parents=True)
    return cache_dir

@pytest.fixture
def isolated_model_dir(tmp_path):
    """Provide isolated model directory for test"""
    model_dir = tmp_path / "models"
    model_dir.mkdir(parents=True)
    return model_dir

@pytest.fixture
def test_environment(monkeypatch, isolated_cache_dir, isolated_model_dir):
    """Set isolated cache and model directories for test"""
    monkeypatch.setenv("STANZA_HOME", str(isolated_cache_dir))
    monkeypatch.setenv("STANZA_RESOURCES_DIR", str(isolated_model_dir))
    return {
        "cache_dir": isolated_cache_dir,
        "model_dir": isolated_model_dir
    }
```

### 2. pre-download Models for CI/CD

In CI/CD pipelines, pre-download required models to avoid runtime downloads:

```yaml
# .github/workflows/tests.yml
- name: Pre-download Stanza models
  run: |
    python -c "import stanza; stanza.download('en')"
```

### 3. PyTorch Best Practices

Use context managers for model loading/saving:

```python
import tempfile
from pathlib import Path

class ModelCheckpoint:
    """Safe model checkpoint management"""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(tempfile.gettempdir())
        self.checkpoint_dir = None
        
    def __enter__(self):
        """Create isolated checkpoint directory"""
        self.checkpoint_dir = Path(tempfile.mkdtemp(dir=self.base_dir))
        return self.checkpoint_dir
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up checkpoint directory"""
        if self.checkpoint_dir and self.checkpoint_dir.exists():
            import shutil
            shutil.rmtree(self.checkpoint_dir)
```

### 4. Override Resource Loading for Tests

Provide test-specific resource configuration:

```python
# stanza/tests/conftest.py
import os
from pathlib import Path

@pytest.fixture(autouse=True)
def test_resources(tmp_path, monkeypatch):
    """Override resource paths for tests"""
    test_cache = tmp_path / "stanza_resources"
    test_cache.mkdir(exist_ok=True)
    
    # Override environment variables
    monkeypatch.setenv("STANZA_HOME", str(test_cache))
    
    # Store reference for cleanup
    yield test_cache
    
    # Auto-cleanup after test
    import shutil
    if test_cache.exists():
        shutil.rmtree(test_cache)
```

### 5. Use pytest's tmp_path and tmpdir

Best practices for test temp files:

```python
def test_with_temp_model(tmp_path):
    """Example using tmp_path fixture"""
    model_path = tmp_path / "model.pt"
    
    # Training saves to isolated location
    trainer.save(model_path)
    
    # Load from same location
    loaded = torch.load(model_path)
    
    # Auto-cleanup when test ends
    assert model_path.exists()
```

### 6. Mark Tests that Use External Resources

```python
pytestmark = [pytest.mark.xfail(reason="Requires cached resources")]

@pytest.mark.integration  # Mark as integration test
def test_train_pipeline():
    pass
```

## Security Considerations

1. Avoid Cache Writes: Don't write to user cache during tests
   - Use tmp_path instead of ~.cache or AppData

2. Prevent Information Leakage: 
   - Don't store sensitive model data in world-readable temp
   - Use restrictive file permissions: `os.chmod(path, 0o600)`

3. Cleanup on Failure:
   - Use try/finally or context managers
   - pytest's tmp_path auto-cleanup handles this

4. Isolation Between Tests:
   - Each test gets its own tmp_path
   - No shared state between test runs

## Implementation Plan

### Phase 1: Fixture Infrastructure (1-2 days)
- [ ] Create isolated temp directory fixtures in conftest.py
- [ ] Add test_environment fixture with environment variable mocking
- [ ] Document fixture usage

### Phase 2: Apply to Trainer Tests (2-3 days)
- [ ] Update stanza/tests/classifiers/test_*.py to use fixtures
- [ ] Update stanza/tests/*/test_trainer.py files
- [ ] Replace all TEST_WORKING_DIR references

### Phase 3: Model Resource Tests (2-3 days)
- [ ] Create resource override fixtures
- [ ] Update tests using stanza.Pipeline
- [ ] Mock resource downloads for CI

### Phase 4: Documentation (1 day)
- [ ] Add testing guide to CONTRIBUTING.md
- [ ] Document fixture patterns
- [ ] Add security best practices

### Phase 5: CI/CD Updates (1 day)
- [ ] Pre-download models in GitHub Actions
- [ ] Set environment variables for isolated testing
- [ ] Add cleanup steps

## Reference Performance Metrics

Expected improvements:
- Test isolation: 100% (each test independent)
- Disk usage: -90% (no persistent cache)
- Cleanup overhead: <100ms (automatic)
- Security score: 100% (no world-readable files)

## Related Issues

- ResourceFileNotFoundError in integration tests
- Test order dependency on cache state
- Windows-specific cache path issues
- CI/CD resource download timeouts

## Tools and References

- pytest.tmp_path: https://docs.pytest.org/en/stable/how-tos/tmp_path.html
- pytest monkeypatch: https://docs.pytest.org/en/stable/reference.html#monkeypatch
- PyTorch checkpoint management: https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_models_across_devices.html
- Python tempfile: https://docs.python.org/3/library/tempfile.html
- Security best practices: https://owasp.org/www-project-secure-coding-practices/

## Next Steps

1. Review and approve fixture design
2. Implement Phase 1 infrastructure
3. Apply to one test module for validation
4. Rollout to remaining test modules
5. Update CI/CD pipelines
6. Document in contribution guidelines
