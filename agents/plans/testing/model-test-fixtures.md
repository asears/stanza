# Model Test Fixtures and Setup Plan

## Problem Statement

Many PyTorch model tests in Stanza depend on:
1. Pretrained embedding files (tiny_emb.pt, tiny_emb.xz, etc.)
2. Downloaded language models
3. External resources (charlm, bert models)
4. Test data files

These dependencies cause tests to fail when:
- Tests run before `stanza/tests/setup.py` executes
- CI/CD environments lack downloaded models
- Test cache directory is not properly initialized
- Developers run tests without setup

## Current State Analysis

### Setup Script (`stanza/tests/setup.py`)

The setup script performs these tasks:
1. Creates directory structure in cache
2. Copies test data files from `stanza/tests/data/` to cache
3. Downloads full language models
4. Downloads CoreNLP

#### Issues with Current Approach:
- Manual execution required before running tests
- Not integrated with pytest discovery
- Downloads large models (100s of MB) for simple unit tests
- Mixes unit test needs with integration test needs
- No fixture-based dependency management

### Files Copied to Cache

```python
# From stanza/tests/data/ to cache/in/
- tiny_emb.txt      # Text format embeddings
- tiny_emb.xz       # Compressed embeddings
- tiny_emb.gz       # Gzip compressed
- tiny_emb.zip      # Zip compressed
- tiny_emb.csv      # CSV format
- tiny_emb.pt       # PyTorch pretrained file
```

### Tests Affected

#### High Dependency Tests (Need setup.py):
```
stanza/tests/constituency/
  - test_lstm_model.py (40+ tests)
  - test_trainer.py (multiple tests)

stanza/tests/ner/
  - test_ner_training.py (multiple tests)

stanza/tests/pos/
  - test_tagger.py (class-based tests)
  - test_xpos_vocab_factory.py

stanza/tests/depparse/
  - test_parser.py (class-based tests)

stanza/tests/lemma_classifier/
  - test_training.py

stanza/tests/common/
  - test_pretrain.py (some tests)
  - test_char_model.py (save/load tests)
```

## Proposed Solutions

### Solution 1: Autouse Session Fixtures (Recommended for CI/CD)

Create session-scoped fixtures that automatically set up test resources.

#### Implementation:

**`stanza/tests/conftest.py`** (pytest configuration):
```python
import pytest
import shutil
from pathlib import Path
from stanza.tests import TEST_WORKING_DIR

@pytest.fixture(scope="session", autouse=True)
def setup_test_cache():
    """
    Automatically set up test cache directory with required files.
    Runs once per test session before any tests execute.
    """
    test_dir = Path(TEST_WORKING_DIR)
    in_dir = test_dir / "in"
    out_dir = test_dir / "out"
    
    # Create directories
    test_dir.mkdir(parents=True, exist_ok=True)
    in_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy test embedding files
    data_dir = Path(__file__).parent / "data"
    for emb_file in data_dir.glob("tiny_emb.*"):
        dest = in_dir / emb_file.name
        if not dest.exists():
            shutil.copy(emb_file, dest)
    
    yield
    
    # Optional: cleanup after all tests
    # Note: Usually we keep cache for debugging
    # shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def tiny_pretrain():
    """
    Provides path to tiny pretrain file for tests.
    Skips tests if file is not available.
    """
    pt_file = Path(TEST_WORKING_DIR) / "in" / "tiny_emb.pt"
    if not pt_file.exists():
        pytest.skip("tiny_emb.pt not available - run test setup first")
    return str(pt_file)
```

#### Benefits:
- Tests work immediately after `pytest` command
- No manual setup required
- Proper pytest integration
- Scoped to session (runs once)
- Can skip gracefully if resources missing

### Solution 2: Lazy Fixture with In-Memory Models

Create models on-demand using minimal data instead of pretrained files.

#### Implementation:

**`stanza/tests/conftest.py`**:
```python
import torch
import numpy as np
from stanza.models.common.pretrain import Pretrain, PretrainedWordVocab
from stanza.models.common.vocab import VOCAB_PREFIX

@pytest.fixture(scope="session")
def minimal_pretrain(tmp_path_factory):
    """
    Create a minimal in-memory pretrain for testing without files.
    """
    # Create minimal vocab and embeddings
    words = ["unban", "mox", "opal"]
    emb_dim = 4
    
    # Create embedding matrix
    emb = torch.zeros((len(VOCAB_PREFIX) + len(words), emb_dim), dtype=torch.float32)
    emb[len(VOCAB_PREFIX):] = torch.tensor([
        [1.0, 2.0, 3.0, 4.0],
        [5.0, 6.0, 7.0, 8.0],
        [9.0, 10.0, 11.0, 12.0]
    ])
    
    # Create vocab
    vocab = PretrainedWordVocab(words)
    
    # Create pretrain-like object
    class MinimalPretrain:
        def __init__(self):
            self.vocab = vocab
            self.emb = emb
    
    return MinimalPretrain()


@pytest.fixture(scope="session")
def minimal_pretrain_file(tmp_path_factory, minimal_pretrain):
    """
    Save minimal pretrain to a temporary file for tests that need file paths.
    """
    tmp_dir = tmp_path_factory.mktemp("pretrain")
    pt_file = tmp_dir / "minimal.pt"
    
    data = {
        'vocab': minimal_pretrain.vocab.state_dict(),
        'emb': minimal_pretrain.emb
    }
    torch.save(data, pt_file, _use_new_zipfile_serialization=False)
    
    return str(pt_file)
```

#### Benefits:
- No external files needed
- Fast test execution
- Isolated test environment
- Works in any environment
- Can be version controlled

#### Drawbacks:
- May not catch issues with real pretrain files
- Requires updating if pretrain format changes

### Solution 3: Conditional Fixtures with Markers

Mark tests by their dependencies and skip appropriately.

#### Implementation:

**`stanza/tests/conftest.py`**:
```python
def pytest_configure(config):
    """Register custom markers for test dependencies"""
    config.addinivalue_line(
        "markers", "pretrain: tests requiring pretrained embeddings"
    )
    config.addinivalue_line(
        "markers", "integration: integration tests requiring full setup"
    )
    config.addinivalue_line(
        "markers", "downloaded_models: tests requiring downloaded models"
    )


@pytest.fixture
def pretrain_file():
    """Pretrain file fixture that skips if not available"""
    from stanza.tests import TEST_WORKING_DIR
    pt_file = Path(TEST_WORKING_DIR) / "in" / "tiny_emb.pt"
    if not pt_file.exists():
        pytest.skip("Pretrain file not available - run setup.py or use --setup flag")
    return str(pt_file)


@pytest.fixture(scope="session")
def require_pretrain():
    """Session fixture that fails fast if pretrain is required but missing"""
    from stanza.tests import TEST_WORKING_DIR
    pt_file = Path(TEST_WORKING_DIR) / "in" / "tiny_emb.pt"
    if not pt_file.exists():
        pytest.exit("Pretrain file required but not found. Run: python stanza/tests/setup.py")
```

**Usage in tests**:
```python
@pytest.mark.pretrain
def test_model_with_pretrain(pretrain_file):
    # Test will skip if pretrain not available
    model = build_model(pretrain_file)
    # ...
```

**Running tests**:
```bash
# Run only tests that don't need pretrain
pytest -m "not pretrain"

# Run all tests including integration
pytest -m "pretrain or not pretrain"
```

### Solution 4: Pytest Plugin for Setup

Create a pytest plugin that runs setup automatically.

#### Implementation:

**`stanza/tests/pytest_stanza.py`**:
```python
import subprocess
import sys
from pathlib import Path

def pytest_configure(config):
    """Run setup if needed before any tests"""
    if config.getoption("--setup", default=False):
        setup_script = Path(__file__).parent / "setup.py"
        print(f"\nRunning test setup: {setup_script}")
        result = subprocess.run([sys.executable, str(setup_script)])
        if result.returncode != 0:
            pytest.exit("Setup failed")


def pytest_addoption(parser):
    """Add --setup option to pytest"""
    parser.addoption(
        "--setup",
        action="store_true",
        default=False,
        help="Run test setup before executing tests"
    )
```

**`conftest.py`**:
```python
pytest_plugins = ["stanza.tests.pytest_stanza"]
```

**Usage**:
```bash
# Run tests with automatic setup
pytest --setup

# Normal run (skips tests if setup not done)
pytest
```

## Recommended Approach

### Phase 1: Immediate Fix (This Week)
1. ✅ Add fixture that checks for pretrain file and skips gracefully
2. ✅ Document skip reason pointing to this plan
3. Create `conftest.py` with autouse session fixture for basic setup

### Phase 2: Robust Fixtures (Next Sprint)
1. Implement Solution 1 (autouse session fixtures)
2. Add Solution 2 (minimal in-memory pretrain) for unit tests
3. Separate unit tests from integration tests using markers

### Phase 3: Advanced Testing (Future)
1. Implement pytest plugin for optional setup
2. Create fixture factories for different model configurations
3. Add fixtures for transformer models (bert, xlnet)
4. Mock external API calls (HuggingFace downloads)

## Testing Patterns for PyTorch Models

### Pattern 1: Model Construction Tests
**Purpose**: Verify model builds with various configurations

```python
def test_model_construction(minimal_pretrain_file):
    """Test model can be constructed"""
    model = build_model(minimal_pretrain_file, '--hidden_size', '128')
    assert model.hidden_size == 128
    assert isinstance(model, LSTMModel)
```

**Benefits**: Fast, no training needed, catches architecture issues

### Pattern 2: Forward Pass Tests
**Purpose**: Verify model can process inputs without crashing

```python
def test_forward_pass(minimal_pretrain_file):
    """Test model forward pass produces correct shape"""
    model = build_model(minimal_pretrain_file)
    states = create_initial_states(model, num_states=2)
    output = model(states)
    assert output.shape == (2, model.num_classes)
```

**Benefits**: Verifies tensor operations, catches shape mismatches

### Pattern 3: Gradient Flow Tests
**Purpose**: Ensure backpropagation works

```python
def test_gradient_flow(minimal_pretrain_file):
    """Test gradients flow through model"""
    model = build_model(minimal_pretrain_file)
    states = create_initial_states(model)
    output = model(states)
    loss = output.sum()
    loss.backward()
    
    # Check gradients exist
    for name, param in model.named_parameters():
        if param.requires_grad:
            assert param.grad is not None, f"No gradient for {name}"
```

**Benefits**: Catches gradient issues early, faster than full training

### Pattern 4: Save/Load Tests
**Purpose**: Verify model serialization

```python
def test_save_load(minimal_pretrain_file, tmp_path):
    """Test model can be saved and loaded"""
    model = build_model(minimal_pretrain_file)
    save_path = tmp_path / "model.pt"
    
    # Save
    torch.save(model.state_dict(), save_path)
    
    # Load
    new_model = build_model(minimal_pretrain_file)
    new_model.load_state_dict(torch.load(save_path))
    
    # Verify parameters match
    for (n1, p1), (n2, p2) in zip(model.named_parameters(), 
                                   new_model.named_parameters()):
        assert n1 == n2
        assert torch.allclose(p1, p2)
```

**Benefits**: Catches serialization issues, version compatibility

### Pattern 5: Determinism Tests
**Purpose**: Verify reproducibility with fixed random seed

```python
def test_determinism(minimal_pretrain_file):
    """Test model produces same results with fixed seed"""
    from stanza.models.common.utils import set_random_seed
    
    set_random_seed(1000)
    model1 = build_model(minimal_pretrain_file)
    output1 = model1(create_initial_states(model1))
    
    set_random_seed(1000)
    model2 = build_model(minimal_pretrain_file)
    output2 = model2(create_initial_states(model2))
    
    assert torch.allclose(output1, output2)
```

**Benefits**: Ensures reproducible experiments, debugging

### Pattern 6: Training Step Tests (Minimal)
**Purpose**: Verify one training step works

```python
def test_training_step(minimal_pretrain_file, mock_data):
    """Test one training step completes"""
    model = build_model(minimal_pretrain_file)
    optimizer = torch.optim.Adam(model.parameters())
    
    states, labels = mock_data
    output = model(states)
    loss = F.cross_entropy(output, labels)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    assert loss.item() > 0  # Loss is computed
```

**Benefits**: Fast smoke test for training loop

## Fixture Organization

### Recommended Structure

```
stanza/tests/
├── conftest.py              # Root fixtures (session-level)
├── setup.py                 # Legacy setup (to be deprecated)
├── data/                    # Test data files
│   ├── tiny_emb.*          # Embedding files
│   └── test_samples/       # Sample training data
├── fixtures/                # Modular fixture definitions
│   ├── __init__.py
│   ├── pretrain.py         # Pretrain-related fixtures
│   ├── models.py           # Model building fixtures
│   ├── data.py             # Data loading fixtures
│   └── transformers.py     # Transformer model fixtures
└── common/
    └── test_pretrain.py    # Tests
```

### Example Fixture Module (`fixtures/pretrain.py`)

```python
import pytest
import torch
from pathlib import Path
from stanza.models.common.pretrain import Pretrain

@pytest.fixture(scope="session")
def tiny_emb_data():
    """Raw embedding data for tests"""
    words = ["unban", "mox", "opal"]
    vectors = [
        [1.0, 2.0, 3.0, 4.0],
        [5.0, 6.0, 7.0, 8.0],
        [9.0, 10.0, 11.0, 12.0]
    ]
    return words, vectors


@pytest.fixture(scope="session")
def tiny_pretrain_memory(tiny_emb_data, tmp_path_factory):
    """In-memory pretrain object"""
    words, vectors = tiny_emb_data
    # Implementation...
    return pretrain_obj


@pytest.fixture(scope="session")
def tiny_pretrain_file(tiny_pretrain_memory, tmp_path_factory):
    """Saved pretrain file"""
    tmp_dir = tmp_path_factory.mktemp("pretrain")
    pt_file = tmp_dir / "tiny.pt"
    # Save pretrain_memory to pt_file
    return str(pt_file)


@pytest.fixture
def pretrain_file_or_skip():
    """Pretrain file or skip test"""
    from stanza.tests import TEST_WORKING_DIR
    pt_file = TEST_WORKING_DIR / "in" / "tiny_emb.pt"
    if not pt_file.exists():
        pytest.skip("Pretrain not available")
    return str(pt_file)
```

## Migration Strategy

### Step 1: Create conftest.py
Create `stanza/tests/conftest.py` with autouse session fixture:
```python
import pytest
import shutil
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def setup_test_resources():
    """Auto-setup test resources before any tests run"""
    from stanza.tests import TEST_WORKING_DIR
    
    test_dir = Path(TEST_WORKING_DIR)
    in_dir = test_dir / "in"
    
    # Create directories
    in_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy embedding files
    data_dir = Path(__file__).parent / "data"
    if data_dir.exists():
        for emb_file in data_dir.glob("tiny_emb.*"):
            dest = in_dir / emb_file.name
            if not dest.exists():
                shutil.copy(emb_file, dest)
```

### Step 2: Update Individual Files
For each test file using pretrain:
1. Import fixture from conftest
2. Update tests to use fixture
3. Remove hardcoded paths
4. Add skip logic if needed

### Step 3: Deprecate setup.py
1. Add deprecation warning to setup.py
2. Document migration in README
3. Eventually remove after fixtures are stable

## Metrics for Success

After implementation:
- ✅ `pytest` works without manual setup
- ✅ Tests skip gracefully if resources unavailable
- ✅ Clear error messages when setup needed
- ✅ Fast unit tests (<1s each)
- ✅ Separate markers for integration tests
- ✅ CI/CD runs smoothly
- ✅ Developer experience improved

## Additional Considerations

### Mocking External Downloads

For tests requiring HuggingFace transformers:
```python
@pytest.fixture
def mock_transformer_download(mocker):
    """Mock transformer downloads for testing"""
    mock_model = create_tiny_mock_model()
    mocker.patch('transformers.AutoModel.from_pretrained', 
                 return_value=mock_model)
    return mock_model
```

### Parallel Test Execution

Ensure fixtures are thread-safe for `pytest-xdist`:
```python
@pytest.fixture(scope="session")
def thread_safe_pretrain(tmp_path_factory, worker_id):
    """Thread-safe pretrain for parallel execution"""
    if worker_id == "master":
        # Single-process mode
        return create_pretrain()
    
    # Multi-process: use worker-specific directory
    root_tmp = tmp_path_factory.getbasetemp().parent
    pretrain_file = root_tmp / f"pretrain_{worker_id}.pt"
    
    # Ensure only one worker creates the file
    with FileLock(str(pretrain_file) + ".lock"):
        if not pretrain_file.exists():
            save_pretrain(pretrain_file)
    
    return str(pretrain_file)
```

### Docker/CI Optimization

```yaml
# .github/workflows/tests.yml
- name: Setup test cache
  uses: actions/cache@v3
  with:
    path: ~/.cache/stanza_test
    key: test-resources-${{ hashFiles('stanza/tests/data/**') }}

- name: Run tests
  run: pytest --setup  # Run with automatic setup
```

## Resources

- [Pytest Fixtures Documentation](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Good Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [PyTorch Testing Best Practices](https://pytorch.org/docs/stable/testing.html)
- [Testing ML Models Guide](https://madewithml.com/courses/mlops/testing/)

## Related Documents

- `agents/plans/testing/test-fixture-improvements.md` - General test fixture improvements
- `agents/plans/testing/test-data-dependencies.md` - Test data management
- `agents/plans/testing/slow-tests-strategy.md` - Test categorization

## Next Steps

1. Implement autouse session fixture in conftest.py
2. Update test_lstm_model.py to use new fixture pattern
3. Create minimal in-memory pretrain fixture
4. Add pytest markers for test categories
5. Update CI/CD to use new testing approach
6. Document testing best practices in CONTRIBUTING.md
