# Pure Python NLP Migration Plan

## Overview

Replace Java-based Stanford CoreNLP dependencies with modern Python NLP libraries to simplify deployment, improve integration, and leverage the rich Python NLP ecosystem.

## Current Java Dependencies Analysis

### Stanford CoreNLP Features Used
1. Constituency Parsing - Alternative parse trees
2. Coreference Resolution - Entity linking across sentences
3. Relation Extraction - IE and KBP triples
4. OpenIE - Open information extraction
5. Pattern Matching - Semgrex (dependency), Tokensregex (token), Tsurgeon (tree surgery)
6. Dependency Graph Enhancement - UD conversion and enhancement
7. Morphological Analysis - Language-specific features

### Integration Overhead
- Java runtime installation and management
- Protocol buffer serialization/deserialization
- Client-server architecture complexity
- Cross-process communication latency
- Memory overhead of running JVM

## Python NLP Ecosystem (2025)

### Modern Foundation Models

#### 1. HuggingFace Transformers
- Status: Industry standard, production-ready
- Models: 200,000+ pre-trained models
- Features: 
  - Token classification (NER, POS)
  - Sequence classification
  - Question answering
  - Text generation
  - Zero-shot classification
- Pros: Active development, extensive model hub, commercial support
- Cons: GPU recommended for large models

#### 2. SpaCy v4+ (2025)
- Status: Production-ready, widely deployed
- Features:
  - Fast tokenization and NER
  - Dependency parsing (neural)
  - Entity linking
  - Text classification
  - Custom pipeline components
  - Efficient multithreading
- Transformer integration: spacy-transformers
- Pros: Fast, batteries-included, excellent docs
- Cons: Limited to supported languages/tasks

#### 3. AllenNLP
- Status: Research-focused but production-ready
- Features:
  - Semantic role labeling
  - Coreference resolution
  - Constituency parsing
  - Open information extraction
  - Textual entailment
- Pros: State-of-art models, research-backed
- Cons: Slower development, some models not maintained

### Specialized Libraries

#### 4. Neuralcoref (Revitalized)
- Alternative: FastCoref (2024+)
- Status: Modern replacement for neuralcoref
- Features: Neural coreference resolution
- Integration: Works with spaCy
- Performance: Faster than Stanford CoreNLP

#### 5. transformers-interpret
- Features: Model interpretability and pattern matching
- Use case: Alternative to Semgrex for pattern-based extraction
- Integration: Works with HuggingFace models

#### 6. TextBlob / NLTK (Modernized)
- Status: Classic libraries with updates
- Features: 
  - POS tagging
  - Parsing
  - Sentiment analysis
  - WordNet integration
- Use case: Fallback for simple tasks

#### 7. Stanza Native Extensions
- Current state: Already implements many features
- Opportunity: Expand native Python implementation
- Advantage: Full control, no external dependencies

### Graph and Pattern Matching

#### 8. NetworkX
- Status: Standard for graph algorithms in Python
- Use case: Dependency graph manipulation
- Features: Graph algorithms, visualization, I/O
- Performance: Pure Python, good for non-critical paths

#### 9. spaCy Matcher / DependencyMatcher
- Status: Production-ready
- Features: 
  - Token patterns (like Tokensregex)
  - Dependency patterns (like Semgrex)
  - Tree patterns
- Pros: Fast, Pythonic API
- Cons: Different pattern syntax than CoreNLP

#### 10. Lark Parser
- Status: Production-ready
- Features: PEG/EBNF parser generator
- Use case: Custom pattern languages, tree manipulation
- Pros: Pure Python, very flexible

### Relation and Information Extraction

#### 11. Rebel (HuggingFace)
- Status: State-of-art (2024)
- Features: Relation extraction with transformers
- Performance: Better than pattern-based approaches
- Use case: Replace CoreNLP relation extraction

#### 12. OpenIE6 (Python port)
- Status: Available in Python
- Features: Open information extraction
- Alternative: Use HuggingFace zero-shot models

#### 13. stanford-openie (Python wrapper)
- Status: Transitional option
- Features: Wraps Java OpenIE but in Python
- Use case: Short-term compatibility

### Constituency Parsing

#### 14. Berkeley Neural Parser (Python)
- Status: Well-maintained
- Features: Fast constituency parsing
- Performance: Competitive with CoreNLP
- Integration: Available via AllenNLP

#### 15. Stanza's Own Constituency Parser
- Status: Already implemented!
- Features: Neural constituency parser
- Advantage: No external dependency needed

### Coreference Resolution

#### 16. NeuralCoref (Legacy) → FastCoref (Modern)
- FastCoref: 
  - Modern replacement (2024+)
  - Faster inference
  - Better accuracy
  - Active maintenance

#### 17. AllenNLP Coref
- Status: Research-grade
- Features: Neural coreference
- Models: Pre-trained on OntoNotes
- Performance: State-of-art

#### 18. Stanza WL-COREF
- Status: Already integrated!
- Advantage: Native implementation available

## Migration Strategy

### Phase 1: Feature Mapping & Prototyping (1 month)

#### Map CoreNLP Features → Python Alternatives

| CoreNLP Feature | Python Alternative | Maturity |
|----------------|-------------------|----------|
| Constituency parsing | Stanza native / AllenNLP | ✅ Ready |
| Coreference | FastCoref / Stanza WL-COREF | ✅ Ready |
| Dependency enhancement | Native Python / NetworkX | ✅ Ready |
| NER | Stanza native / spaCy | ✅ Ready |
| OpenIE | OpenIE6-py / Rebel | ⚠️ Needs testing |
| Semgrex | spaCy DependencyMatcher | ⚠️ Syntax different |
| Tokensregex | spaCy Matcher / regex | ✅ Ready |
| Tsurgeon | Custom + Lark | 🔨 Build needed |

#### Prototype Critical Features

```python
# Example: Dependency pattern matching (Semgrex alternative)
import spacy
from spacy.matcher import DependencyMatcher

nlp = spacy.load("en_core_web_trf")
matcher = DependencyMatcher(nlp.vocab)

# Pattern: subject <- verb -> object
pattern = [
    {
        "RIGHT_ID": "verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
    },
    {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "subject",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "object",
        "RIGHT_ATTRS": {"DEP": "dobj"}
    }
]

matcher.add("SVO", [pattern])
```

### Phase 2: Core Infrastructure (2 months)

#### Unified API Layer

```python
# stanza/backends/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class NLPBackend(ABC):
    @abstractmethod
    def parse_constituency(self, text: str) -> Any:
        pass
    
    @abstractmethod
    def resolve_coreference(self, doc: Any) -> List[Dict]:
        pass
    
    @abstractmethod
    def extract_relations(self, doc: Any) -> List[Dict]:
        pass
    
    @abstractmethod
    def match_pattern(self, doc: Any, pattern: str) -> List[Any]:
        pass

# stanza/backends/java_backend.py
class JavaBackend(NLPBackend):
    """Existing CoreNLP implementation"""
    def __init__(self):
        from stanza.server import CoreNLPClient
        self.client = CoreNLPClient(...)
    
    # Existing implementations...

# stanza/backends/python_backend.py
class PythonBackend(NLPBackend):
    """New pure-Python implementation"""
    def __init__(self):
        import spacy
        from fastcoref import FCoref
        self.nlp = spacy.load("en_core_web_trf")
        self.coref_model = FCoref(...)
    
    def resolve_coreference(self, doc):
        # Use FastCoref
        return self.coref_model.predict(doc.text)
    
    # New implementations...

# stanza/backends/factory.py
def get_backend(backend: str = "auto") -> NLPBackend:
    if backend == "java":
        return JavaBackend()
    elif backend == "python":
        return PythonBackend()
    elif backend == "auto":
        try:
            return PythonBackend()
        except ImportError:
            return JavaBackend()
```

#### Configuration System

```python
# Add to stanza config
BACKEND_CONFIG = {
    "default_backend": "python",  # or "java"
    "fallback_to_java": True,
    "backends": {
        "python": {
            "coref": "fastcoref",  # or "allennlp" or "wl-coref"
            "constituency": "stanza",  # or "allennlp"
            "openie": "rebel",  # or "openie6"
            "pattern_matcher": "spacy",
        },
        "java": {
            "use_corenlp": True,
        }
    }
}
```

### Phase 3: Feature Implementation (4-6 months)

#### Priority 1: Pattern Matching (2 months)

Tokensregex Alternative
```python
# stanza/pattern/token_matcher.py
import spacy
from spacy.matcher import Matcher

class TokenRegexMatcher:
    """Drop-in replacement for CoreNLP TokensRegex"""
    
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab)
    
    def add_pattern(self, name: str, pattern: str):
        # Convert TokensRegex syntax to spaCy pattern
        spacy_pattern = self._convert_pattern(pattern)
        self.matcher.add(name, [spacy_pattern])
    
    def _convert_pattern(self, tokensregex: str) -> List[Dict]:
        # Pattern conversion logic
        # [word="the"] [pos="NN"] -> [{"LOWER": "the"}, {"POS": "NOUN"}]
        pass
```

Semgrex Alternative
```python
# stanza/pattern/dependency_matcher.py
from spacy.matcher import DependencyMatcher

class SemgrexMatcher:
    """Drop-in replacement for CoreNLP Semgrex"""
    
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = DependencyMatcher(nlp.vocab)
    
    def add_pattern(self, name: str, semgrex: str):
        # Convert Semgrex syntax to spaCy pattern
        spacy_pattern = self._convert_semgrex(semgrex)
        self.matcher.add(name, [spacy_pattern])
    
    def _convert_semgrex(self, semgrex: str) -> List[Dict]:
        # Pattern conversion logic
        # {word:verb} >nsubj {word:subject}
        pass
```

#### Priority 2: Coreference Resolution (1 month)

```python
# stanza/coref/python_resolver.py
from fastcoref import FCoref

class PythonCorefResolver:
    def __init__(self, model_name: str = "biu-nlp/f-coref"):
        self.model = FCoref(model_name_or_path=model_name)
    
    def resolve(self, text: str) -> Dict:
        predictions = self.model.predict(texts=[text])
        
        # Convert to CoreNLP-compatible format
        chains = []
        for cluster_id, cluster in enumerate(predictions[0].get_clusters()):
            chain = {
                "chainID": cluster_id,
                "mentions": [
                    {
                        "text": text[start:end],
                        "startIndex": start,
                        "endIndex": end,
                    }
                    for start, end in cluster
                ]
            }
            chains.append(chain)
        
        return {"corefChains": chains}
```

#### Priority 3: OpenIE (2 months)

```python
# stanza/openie/python_extractor.py
from transformers import pipeline

class PythonOpenIE:
    def __init__(self):
        # Use Rebel or similar model
        self.extractor = pipeline(
            "text2text-generation",
            model="Babelscape/rebel-large"
        )
    
    def extract_triples(self, text: str) -> List[Dict]:
        # Extract relations
        outputs = self.extractor(text)
        
        # Parse and format
        triples = []
        for output in outputs:
            # Convert to (subject, relation, object) format
            triple = self._parse_rebel_output(output['generated_text'])
            triples.append({
                "subject": triple[0],
                "relation": triple[1],
                "object": triple[2],
                "confidence": output.get('score', 1.0)
            })
        
        return triples
```

#### Priority 4: Tree Surgery (Tsurgeon alternative) (1 month)

```python
# stanza/tree/python_surgeon.py
from lark import Lark, Transformer

class TreeSurgeon:
    """Python implementation of Tsurgeon operations"""
    
    def __init__(self):
        # Define grammar for tree patterns
        self.parser = Lark("""
            start: operation+
            operation: delete | move | relabel | insert
            delete: "delete" pattern
            move: "move" pattern "to" pattern
            relabel: "relabel" pattern "to" label
            // ... more operations
        """)
    
    def apply_operations(self, tree: Any, operations: str) -> Any:
        parsed = self.parser.parse(operations)
        for op in parsed.children:
            tree = self._apply_operation(tree, op)
        return tree
```

### Phase 4: Integration & Testing (2 months)

#### Backward Compatibility Layer

```python
# stanza/server/compat.py
"""Compatibility layer for existing CoreNLP client code"""

class CoreNLPClient:
    """Drop-in replacement using Python backend"""
    
    def __init__(self, backend="python", kwargs):
        if backend == "python":
            from stanza.backends import PythonBackend
            self.backend = PythonBackend()
        else:
            from stanza.server.client import CoreNLPClient as JavaClient
            self.backend = JavaClient(kwargs)
    
    def annotate(self, text, properties=None, kwargs):
        # Route to appropriate backend
        return self.backend.annotate(text, properties, kwargs)
```

#### Testing Strategy

```python
# tests/test_backend_parity.py
import pytest
from stanza.backends import JavaBackend, PythonBackend

@pytest.mark.parametrize("backend", [JavaBackend(), PythonBackend()])
def test_coref_resolution(backend):
    """Ensure both backends produce similar results"""
    text = "Barack Obama was born in Hawaii. He became president in 2009."
    
    result = backend.resolve_coreference(text)
    
    # Check that "He" is linked to "Barack Obama"
    assert any(
        "Barack Obama" in str(chain) and "He" in str(chain)
        for chain in result['corefChains']
    )

@pytest.mark.parametrize("backend", [JavaBackend(), PythonBackend()])
def test_pattern_matching(backend):
    """Test pattern matching compatibility"""
    text = "The cat sat on the mat."
    pattern = "[word='cat']"  # Simple pattern
    
    matches = backend.match_pattern(text, pattern)
    
    assert len(matches) == 1
    assert "cat" in matches[0]['text']
```

### Phase 5: Performance Optimization (1 month)

#### Caching & Batching

```python
# stanza/backends/optimized.py
from functools import lru_cache
from typing import List
import torch

class OptimizedPythonBackend(PythonBackend):
    def __init__(self, batch_size=32, cache_size=1000):
        super().__init__()
        self.batch_size = batch_size
        self._coref_cache = {}
    
    def resolve_coreference_batch(self, texts: List[str]) -> List[Dict]:
        """Batch processing for efficiency"""
        # Check cache
        uncached = [t for t in texts if t not in self._coref_cache]
        
        if uncached:
            # Process in batches
            results = []
            for i in range(0, len(uncached), self.batch_size):
                batch = uncached[i:i + self.batch_size]
                batch_results = self.coref_model.predict(texts=batch)
                results.extend(batch_results)
            
            # Update cache
            for text, result in zip(uncached, results):
                self._coref_cache[text] = result
        
        return [self._coref_cache[t] for t in texts]
```

## Python Library Requirements

### Core Dependencies

```toml
# Add to pyproject.toml [project.optional-dependencies]

python-backend = [
    # Core NLP
    "spacy>=3.7.0",
    "transformers>=4.40.0",
    "torch>=2.0.0",
    
    # Specialized models
    "fastcoref>=2.1.0",                    # Coreference
    "allennlp>=2.10.0",                    # Advanced NLP (optional)
    "allennlp-models>=2.10.0",            # Pre-trained models (optional)
    
    # Pattern matching & parsing
    "lark>=1.1.0",                        # Parser generator
    
    # Relation extraction
    "sentence-transformers>=2.5.0",       # Embeddings
    
    # Graph algorithms
    "networkx>=3.0",                      # Graph manipulation
    
    # Performance
    "numpy>=1.24.0",
    "scipy>=1.10.0",
    
    # Optional: specific models
    "en-core-web-trf @ https://...",      # spaCy transformer model
]
```

### Model Downloads

```python
# stanza/backends/setup.py
def download_python_models():
    """Download required models for Python backend"""
    import spacy
    from huggingface_hub import snapshot_download
    
    # spaCy models
    spacy.cli.download("en_core_web_trf")
    
    # HuggingFace models
    snapshot_download("biu-nlp/f-coref")
    snapshot_download("Babelscape/rebel-large")
    
    # AllenNLP models
    # Automatically downloaded on first use
```

## Benefits

### Deployment Simplification
- No Java runtime: Eliminates JRE dependency
- Smaller footprint: Typical reduction of 200-500 MB
- Faster startup: No JVM warmup (5-10x faster)
- Single language: Easier debugging and profiling
- Container optimization: Smaller Docker images

### Development Velocity
- Native Python: No serialization overhead
- Rich debugging: Python debuggers work seamlessly
- Easier testing: pytest, fixtures, mocking
- Type hints: Better IDE support with mypy
- Jupyter integration: Interactive development

### Performance
- Batch processing: Easier to implement
- GPU utilization: Direct PyTorch/TF integration
- Memory efficiency: No cross-process communication
- Parallelization: multiprocessing, threading
- Modern hardware: Better use of modern accelerators

### Maintenance
- Single codebase: No Java maintenance
- Better documentation: Python docstrings, Sphinx
- Community contributions: Lower barrier to entry
- Dependency management: pip/uv/poetry
- CI/CD simplification: One language to test

## Challenges & Mitigations

### Challenge 1: Feature Parity
Issue: Some CoreNLP features may not have exact Python equivalents

Mitigation:
- Implement critical features only
- Provide fallback to Java for rare features
- Document feature differences clearly
- Contribute to Python NLP libraries to close gaps

### Challenge 2: Pattern Syntax Incompatibility
Issue: Semgrex/Tokensregex syntax differs from spaCy

Mitigation:
- Build pattern converters (Semgrex → spaCy)
- Provide migration guide for users
- Support both syntaxes initially
- Deprecate old syntax gradually

### Challenge 3: Model Accuracy
Issue: Python models may have different accuracy profiles

Mitigation:
- Extensive accuracy testing
- Document accuracy trade-offs
- Allow model selection
- Provide benchmarks

### Challenge 4: Breaking Changes
Issue: Users depend on CoreNLP behavior

Mitigation:
- Feature flags for backends
- Deprecation warnings
- Compatibility mode
- Extensive documentation

## Migration Paths

### Option A: Big Bang (Not Recommended)
- Replace all Java dependencies at once
- High risk, high disruption
- Clear timeline

### Option B: Gradual Migration (Recommended)
- Phase 1: Add Python backend option
- Phase 2: Make Python default, Java fallback
- Phase 3: Deprecate Java backend
- Phase 4: Remove Java support

### Option C: Hybrid Approach
- Keep Java for complex features
- Use Python for common features
- Eventual full migration

## Timeline Estimate

- Phase 1 (Feature Mapping): 1 month
- Phase 2 (Infrastructure): 2 months
- Phase 3 (Implementation): 6 months
- Phase 4 (Testing): 2 months
- Phase 5 (Optimization): 1 month
- Total: 12 months to stable release

## Resource Requirements

- 2-3 Python/NLP engineers: Full-time
- 1 ML engineer: Part-time (model evaluation)
- 1 DevOps engineer: Part-time (deployment)
- GPU resources: For testing transformer models
- Community engagement: For testing and feedback

## Success Metrics

1. Installation success rate: >95% (vs ~70% with Java)
2. Startup time: <500ms (vs ~5s with Java)
3. Memory overhead: <2GB (vs ~4GB with Java)
4. Accuracy: >95% parity with Java on benchmarks
5. User adoption: 50% using Python backend within 6 months

## Recommended Stack (2025)

```python
PYTHON_BACKEND_STACK = {
    "core_nlp": "spacy>=3.7",               # Fast, efficient
    "transformers": "transformers>=4.40",    # Model hub
    "coref": "fastcoref>=2.1",              # Modern coreref
    "patterns": "spacy.matcher",            # Pattern matching
    "graphs": "networkx>=3.0",              # Graph algorithms
    "parsing": "lark>=1.1",                 # Custom patterns
    "relations": "sentence-transformers",    # Embeddings
    "constituency": "stanza.native",        # Already have it!
}
```

## Next Steps

1. Stakeholder buy-in: Present plan to team
2. Proof of concept: Build minimal working example
3. Benchmark: Compare Python vs Java on key tasks
4. User survey: Gauge interest in Python-only version
5. Roadmap: Finalize timeline and resources
6. Implementation: Start Phase 1

## References

- [spaCy](https://spacy.io/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [FastCoref](https://github.com/shon-otmazgin/fastcoref)
- [AllenNLP](https://allenai.org/allennlp)
- [Rebel (Relation Extraction)](https://huggingface.co/Babelscape/rebel-large)
- [Lark Parser](https://github.com/lark-parser/lark)
- [NetworkX](https://networkx.org/)
