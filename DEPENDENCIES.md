# Stanza Project Dependencies Reference

List of all dependencies, file types, and external tools used in the Stanza project.

<style>
  .pkg-manager-toggle {
    display: flex;
    gap: 10px;
    margin: 20px 0;
    align-items: center;
  }
  .toggle-button {
    padding: 8px 16px;
    border: 2px solid #d0d0d0;
    background: white;
    cursor: pointer;
    border-radius: 4px;
    font-weight: 500;
    transition: all 0.3s;
  }
  .toggle-button.active {
    background: #0969da;
    color: white;
    border-color: #0969da;
  }
  .install-cmd {
    background: #f6f8fa;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 12px;
    font-family: monospace;
    overflow-x: auto;
  }
  .uv-only { display: none; }
  .uv-only.active { display: inline; }
  .pip-only { display: inline; }
  .pip-only.not-active { display: none; }
</style>

<div class="pkg-manager-toggle">
  <label>Package Manager:</label>
  <button class="toggle-button active" onclick="togglePkgManager('pip')">pip</button>
  <button class="toggle-button" onclick="togglePkgManager('uv')">uv (Recommended)</button>
</div>

<script>
function togglePkgManager(manager) {
  // Update button states
  document.querySelectorAll('.toggle-button').forEach(btn => {
    btn.classList.remove('active');
  });
  event.target.classList.add('active');
  
  // Toggle command visibility
  if (manager === 'uv') {
    document.querySelectorAll('.uv-only').forEach(el => el.classList.add('active'));
    document.querySelectorAll('.pip-only').forEach(el => el.classList.add('not-active'));
  } else {
    document.querySelectorAll('.uv-only').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.pip-only').forEach(el => el.classList.remove('not-active'));
  }
}
</script>

## Table of Contents
- [Core Dependencies](#core-dependencies)
- [Optional Dependencies](#optional-dependencies)
- [Development Dependencies](#development-dependencies)
- [File Type Summary](#file-type-summary)
- [External Tools and Integrations](#external-tools-and-integrations)

---

## Core Dependencies

These packages are required for basic Stanza functionality:

| Package | Version | Purpose | Type |
|---------|---------|---------|------|
| `numpy` | Latest | Numerical computing and array operations | Core |
| `torch` | >=1.13.0 | Deep learning framework for neural models | Core |
| `protobuf` | >=3.15.0 | Serialization and data interchange format | Core |
| `requests` | Latest | HTTP library for network requests | Core |
| `tqdm` | Latest | Progress bar utilities | Core |
| `networkx` | Latest | Graph data structure library | Core |
| `emoji` | Latest | Emoji handling utilities | Core |
| `platformdirs` | Latest | Platform-specific directory paths | Core |
| `udtools` | >=0.2.4 | Universal Dependencies tools | Core |
| `tomli` | Latest | TOML file parsing (Python < 3.11) | Core |

---

## Optional Dependencies

Install with selected package manager below:

### Transformer Models
**Install:**

<div class="install-cmd pip-only">
pip install stanza[transformers]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[transformers]
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| `transformers` | >=3.0.0 | Hugging Face transformer models and utilities |
| `peft` | >=0.6.1 | Parameter-Efficient Fine-Tuning for large models |

### Language-Specific Tokenizers
**Install:**

<div class="install-cmd pip-only">
pip install stanza[tokenizers]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[tokenizers]
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| `jieba` | Latest | Chinese text segmentation |
| `pythainlp` | Latest | Thai language processing |
| `python-crfsuite` | Latest | Conditional Random Fields (wrapper) |
| `spacy` | Latest | Natural Language Processing library |
| `sudachidict_core` | Latest | Sudachi dictionary (core) |
| `sudachipy` | Latest | Japanese morphological analyzer |

### Dataset Processing
**Install:**

<div class="install-cmd pip-only">
pip install stanza[datasets]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[datasets]
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| `datasets` | Latest | Hugging Face datasets library |

### Visualization
**Install:**

<div class="install-cmd pip-only">
pip install stanza[visualization]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[visualization]
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| `spacy` | Latest | NLP visualization components |
| `streamlit` | Latest | Interactive web app framework |
| `ipython` | Latest | Interactive computing environment |

### Morphological Segmentation
**Install:**

<div class="install-cmd pip-only">
pip install stanza[morphseg]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[morphseg]
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| `morphseg` | >=0.2.0 | Morphological segmentation library |

### Development
**Install:**

<div class="install-cmd pip-only">
pip install stanza[dev]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[dev]
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| `check-manifest` | Latest | Verify MANIFEST.in file |

### Testing
**Install:**

<div class="install-cmd pip-only">
pip install stanza[test]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[test]
</div>

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | Latest | Testing framework |
| `coverage` | Latest | Code coverage measurement |

### All Extras
**Install:**

<div class="install-cmd pip-only">
pip install stanza[all]
</div>
<div class="install-cmd uv-only">
uv pip install stanza[all]
</div>

Installs all optional dependencies.

---

## Development Dependencies

For code quality and development:

| Tool | Purpose | Integration |
|------|---------|-------------|
| `ruff` | Fast Python linter and formatter | GitHub Actions, local checks |
| `mypy` | Static type checker for Python | GitHub Actions, local checks |
| `pytest` | Unit testing framework | CI/CD pipeline |
| `coverage` | Code coverage analysis | CI/CD pipeline |

---

## File Type Summary

Complete inventory of file types in the repository:

| Extension | Count | Purpose | Examples |
|-----------|-------|---------|----------|
| `.py` | 547 | Python source code | Core modules, models, tests |
| `.md` | 8 | Markdown documentation | README, CONTRIBUTING, TERMS |
| `.ipynb` | 6 | Jupyter Notebooks | Demo and tutorial notebooks |
| `.txt` | 5 | Text files | Test data, configuration |
| `.ttf` | 3 | TrueType fonts | UI display fonts |
| `.sh` | 2 | Bash shell scripts | Environment setup, downloads |
| `.ps1` | 2 | PowerShell scripts | Windows environment setup |
| `.yml` | 2 | YAML configuration | GitHub workflows, CI config |
| `.yaml` | 1 | YAML configuration | Additional configs |
| `.js` | 2 | JavaScript files | Web UI and visualization |
| `.css` | 1 | Stylesheet | Web UI styling |
| `.html` | 1 | HTML markup | Web interface template |
| `.gif` | 1 | Animation/Image | Documentation media |
| `.png` | 1 | PNG image | Documentation media |
| `.json` | 1 | JSON data | Configuration/data interchange |
| `.proto` | 1 | Protocol Buffers | CoreNLP data format definition |
| `.toml` | 1 | TOML configuration | Coref model configuration |
| `.csv` | 1 | CSV data | Tabular data files |
| `.pt` | 1 | PyTorch model | Serialized neural network |
| `.dat` | 1 | Binary data | Serialized data |
| `.zip` | 2 | Compressed archives | Package distributions |
| `.xz` | 1 | XZ compression | Compressed word vectors |
| `.gz` | 1 | Gzip compression | Compressed archives |
| `.conllu` | 1 | CoNLL-U format | Annotation data |
| `.ini` | 1 | INI configuration | Settings files |
| `.properties` | 1 | Java properties | Configuration |
| `.gitignore` | 1 | Git ignore rules | Repository rules |
| (No extension) | 2 | Configuration files | dotfiles, scripts |

---

## External Tools and Integrations

### Language Processing Tools
| Tool | Language | Integration | Purpose |
|------|----------|-----------|---------|
| Jieba | Chinese | Optional (tokenizers) | Text segmentation |
| PyThaiNLP | Thai | Optional (tokenizers) | Thai NLP processing |
| Sudachi | Japanese | Optional (tokenizers) | Japanese morphological analysis |
| spaCy | Multi-language | Optional (tokenizers, visualization) | NLP processing and visualization |

### Frameworks and Libraries
| Framework | Type | Purpose | Version |
|-----------|------|---------|---------|
| PyTorch | Deep Learning | Neural network implementation | >=1.13.0 |
| CUDA | GPU Computing | GPU acceleration support | Optional |
| Transformers (HF) | NLP Models | Pre-trained language models | >=3.0.0 |
| NetworkX | Graph | Graph algorithms and structures | Latest |
| tqdm | Utilities | Progress tracking | Latest |

### Data and Serialization
| Format | Tool | Purpose |
|--------|------|---------|
| Protocol Buffers | protobuf | Stanford CoreNLP integration |
| CoNLL-U | Universal Dependencies | Annotation standard |
| TOML | tomli | Configuration parsing |
| JSON | Standard library | Data interchange |

### Continuous Integration
| Service | Purpose | Config File |
|---------|---------|-------------|
| GitHub Actions | CI/CD pipeline | `.github/workflows/stanza-tests.yaml` |
| Dependabot | Dependency updates | `.github/dependabot.yml` |
| pytest | Test execution | `stanza/tests/pytest.ini` |

---

## Python Version Support

| Version | Supported | Details |
|---------|-----------|---------|
| 3.9 | ✅ Yes | Minimum required version |
| 3.10 | ✅ Yes | Fully supported |
| 3.11 | ✅ Yes | Fully supported (tomli not needed) |
| 3.12 | ✅ Yes | Fully supported |
| 3.13 | ✅ Yes | Fully supported |

---

## Installation Profiles

### Minimal Installation
<div class="install-cmd pip-only">
pip install stanza
</div>
<div class="install-cmd uv-only">
uv pip install stanza
</div>

Installs only core dependencies for basic NLP tasks.

### Development Environment
<div class="install-cmd pip-only">
pip install -e ".[dev,test,transformers,tokenizers]"
</div>
<div class="install-cmd uv-only">
uv pip install -e ".[dev,test,transformers,tokenizers]"
</div>

Full development setup with testing and optional features.

### Full Installation (All Features)
<div class="install-cmd pip-only">
pip install -e ".[dev,test,transformers,datasets,tokenizers,visualization,morphseg]"
</div>
<div class="install-cmd uv-only">
uv pip install -e ".[dev,test,transformers,datasets,tokenizers,visualization,morphseg]"
</div>

Installs all optional features for maximum functionality.

### Using UV (Recommended for Performance)
<div class="install-cmd uv-only active">
uv pip install stanza
uv pip install stanza[all]
</div>
<div class="install-cmd pip-only">
Faster dependency resolution and installation using `uv`.
</div>

---

## Dependency Management

### Using pip (Traditional)
- **File:** `setup.py`
- **Format:** Python setup configuration
- **Update:** Manual or via Dependabot

### Using uv (Modern, Recommended)
- **Faster:** 5-10x faster than pip
- **Reliable:** Deterministic dependency resolution
- **Integration:** Supported by Dependabot
- **Install:** `pip install uv` then `uv pip install stanza`

### Dependabot Configuration
Located in `.github/dependabot.yml`, configured to:
- Check for updates: **Weekly (Mondays at 3:00 AM UTC)**
- Track ecosystems: pip, github-actions, uv
- Automatic PR creation with detailed changelogs
- Label and review assignments
- Ignore pre-release versions for stability

---

## Security Considerations

### Vulnerability Scanning
- Dependabot monitors all dependencies for CVE vulnerabilities
- Security alerts trigger automatic PR creation
- GitHub Security tab shows all known issues

### Pinned Versions (Critical Dependencies)
- `torch>=1.13.0` - Core ML framework with security updates
- `protobuf>=3.15.0` - Serialization security
- `peft>=0.6.1` - Model safety features

### Recommended Practices
1. Review Dependabot PRs before merging
2. Keep torch and protobuf updated
3. Monitor GitHub Security tab regularly
4. Run tests on PR branches before merge

---

## Notable Dependencies

### PyTorch (torch >=1.13.0)
- **Size:** Large (~1-2 GB with CUDA support)
- **Purpose:** Core neural network framework
- **Note:** CPU-only builds available for smaller installations

### Transformers (Optional)
- **Size:** ~500 MB
- **Purpose:** Pre-trained language models from Hugging Face
- **Note:** Only needed for transformer-based features

### Datasets (Optional)
- **Size:** ~100 MB
- **Purpose:** Loading and processing NLP datasets
- **Note:** Only needed for dataset handling

---

## Related Documentation

- [Stanza GitHub Repository](https://github.com/stanfordnlp/stanza)
- [Stanza Official Website](https://stanfordnlp.github.io/stanza/)
- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)
- [Universal Dependencies Format](https://universaldependencies.org/format.html)
- [uv Package Manager](https://github.com/astral-sh/uv)

---

*Last Updated: February 28, 2026*  
*Repository: stanfordnlp/stanza*  
*Python Versions Supported: 3.9, 3.10, 3.11, 3.12, 3.13*
