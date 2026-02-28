# Rust-Based NLP Migration Plan

## Overview

Migrate from Java-based Stanford CoreNLP dependencies to Rust-based NLP libraries for improved performance, memory safety, and reduced deployment complexity.

## Current Java Dependencies

### Stanford CoreNLP Integration
- Purpose: Advanced NLP features beyond Stanza's native capabilities
- Components:
  - Constituency parsing (alternative to neural parser)
  - Coreference resolution
  - Relation extraction
  - OpenIE (open information extraction)
  - Semgrex/Ssurgeon pattern matching
  - Tokensregex pattern matching
  - Dependency graph manipulation

### Interface Points
- `stanza/server/` - Client-server communication
- `stanza/protobuf/CoreNLP_pb2.py` - Protocol buffer definitions
- Java runtime requirement for CoreNLP server

### Pain Points
- JVM installation required
- Large memory footprint
- Slower startup times
- Cross-language serialization overhead
- Platform-specific Java distribution issues

## Rust NLP Ecosystem (2025)

### Core Libraries

#### 1. Candle + Burn (Deep Learning)
- Candle: Minimalist ML framework from HuggingFace (Rust)
- Burn: Deep learning framework with PyTorch-like API
- Use case: Reimplementing neural models (LSTM, transformers)
- Pros: Fast inference, small binary size, GPU support
- Cons: Smaller ecosystem than PyTorch

#### 2. Tokenizers (HuggingFace)
- Status: Production-ready, used by Python transformers library
- Features: Fast BPE, WordPiece, Unigram tokenization
- Use case: Replace CoreNLP tokenization
- Performance: 10-100x faster than Python implementations

#### 3. rust-bert
- Status: Mature Rust wrapper around libtorch
- Features: BERT, GPT-2, RoBERTa, etc.
- Use case: Transformer-based NLP tasks
- Pros: Native Rust, good performance
- Cons: Still depends on libtorch C++ library

#### 4. Linfa (Machine Learning)
- Status: Growing ecosystem
- Features: Traditional ML algorithms, similar to scikit-learn
- Use case: Feature-based classifiers
- Pros: Pure Rust, no external dependencies

#### 5. RegexParsing / Pest
- Status: Production-ready
- Features: PEG parser generator
- Use case: Replace Semgrex/Tokensregex pattern matching
- Pros: Type-safe, fast, expressive

### Specialized NLP Libraries

#### 6. rust-stemmers
- Features: Porter, Lancaster, Snowball stemmers
- Use case: Morphological processing

#### 7. whatlang-rs
- Features: Fast language detection
- Use case: Replace CoreNLP language detection

#### 8. rust-punkt
- Features: Sentence boundary detection
- Use case: Replace CoreNLP sentence splitting

#### 9. tantivy
- Features: Full-text search engine (like Lucene but in Rust)
- Use case: Text indexing and search
- Pros: Fast, low memory, no JVM

## Migration Strategy

### Phase 1: Assessment (1-2 months)

1. Identify CoreNLP usage patterns
   - Audit all uses of `stanza.server` module
   - Categorize features by criticality
   - Measure performance baselines

2. Prototype critical paths
   - Build Rust-Python bindings with PyO3
   - Benchmark Rust implementations vs Java
   - Validate accuracy on test datasets

3. Define success criteria
   - Performance targets (latency, throughput, memory)
   - Accuracy requirements (F1, precision, recall)
   - API compatibility guarantees

### Phase 2: Core Infrastructure (2-3 months)

1. PyO3 Bridge Architecture
   ```rust
   // stanza-rs/src/lib.rs
   use pyo3::prelude::*;
   
   #[pyclass]
   struct RustNLPProcessor {
       // Internal Rust state
   }
   
   #[pymethods]
   impl RustNLPProcessor {
       #[new]
       fn new() -> Self { ... }
       
       fn process(&self, text: &str) -> PyResult<ProcessedDoc> { ... }
   }
   
   #[pymodule]
   fn stanza_rs(_py: Python, m: &PyModule) -> PyResult<()> {
       m.add_class::<RustNLPProcessor>()?;
       Ok(())
   }
   ```

2. Build System Integration
   - Add `maturin` or `setuptools-rust` to build pipeline
   - Create wheel distributions with compiled binaries
   - Support cross-compilation for major platforms

3. Data Structures
   - Define Rust equivalents of core types
   - Implement zero-copy conversions where possible
   - Use `pyo3` for efficient Python interop

### Phase 3: Feature Migration (4-6 months)

#### Priority 1: Tokenization & Sentence Splitting
```rust
// Use tokenizers crate
use tokenizers::{Tokenizer, models::bpe::BPE};

pub fn tokenize_rust(text: &str) -> Vec<String> {
    let tokenizer = Tokenizer::from_pretrained("bert-base-uncased", None).unwrap();
    tokenizer.encode(text, false)
        .unwrap()
        .get_tokens()
        .to_vec()
}
```

#### Priority 2: Pattern Matching (Semgrex/Tokensregex)
```rust
// Use pest for grammar-based parsing
use pest::Parser;

#[derive(Parser)]
#[grammar = "semgrex.pest"]
struct SemgrexParser;

pub fn match_pattern(graph: &DependencyGraph, pattern: &str) -> Vec<Match> {
    let pairs = SemgrexParser::parse(Rule::pattern, pattern).unwrap();
    // Pattern matching logic
}
```

#### Priority 3: Dependency Parsing
- Reimplement graph manipulation in Rust
- Use efficient graph libraries (petgraph)
- Maintain compatibility with UD formats

#### Priority 4: Coreference Resolution
- Port deep learning models to Candle/Burn
- Use rust-bert for transformer components
- Benchmark against WL-COREF

### Phase 4: Advanced Features (3-4 months)

1. Relation Extraction
   - Pattern-based extractors in Rust
   - Neural relation models with rust-bert

2. OpenIE
   - Port OpenIE algorithms to Rust
   - Optimize for performance

3. Parsing Infrastructure
   - Enhanced dependency graph utilities
   - Tree manipulation libraries

### Phase 5: Testing & Validation (2-3 months)

1. Accuracy Testing
   - Run full test suite against Rust implementations
   - Compare outputs with Java CoreNLP
   - Measure regression on benchmarks

2. Performance Testing
   - Latency benchmarks
   - Memory profiling
   - Throughput stress tests

3. Integration Testing
   - End-to-end pipeline tests
   - Backward compatibility checks
   - Multi-platform validation

## Technical Architecture

### Rust Package Structure
```
stanza-rs/
├── Cargo.toml
├── src/
│   ├── lib.rs              # PyO3 bindings
│   ├── tokenization/
│   │   ├── mod.rs
│   │   └── sentence_split.rs
│   ├── parsing/
│   │   ├── dependency.rs
│   │   ├── constituency.rs
│   │   └── patterns.rs
│   ├── coref/
│   │   └── mod.rs
│   ├── relation/
│   │   └── extraction.rs
│   └── utils/
│       ├── graph.rs
│       └── io.rs
├── benches/
├── tests/
└── python/
    └── stanza_rs.pyi        # Type stubs
```

### Python Integration
```python
# After phase 1
try:
    from stanza_rs import RustProcessor
    USE_RUST_BACKEND = True
except ImportError:
    USE_RUST_BACKEND = False

class Processor:
    def __init__(self):
        if USE_RUST_BACKEND:
            self._impl = RustProcessor()
        else:
            self._impl = JavaProcessor()
```

## Benefits

### Performance
- 3-10x faster processing for CPU-bound tasks
- 50-80% memory reduction vs JVM
- Instant startup (no JVM warmup)
- Native binary distribution (no runtime installation)

### Deployment
- Single binary for each platform
- No Java runtime dependency
- Smaller Docker images (100-500MB savings)
- Easier cross-compilation

### Maintenance
- Memory safety (no null pointer exceptions, use-after-free)
- Fearless concurrency (compiler-enforced thread safety)
- Better error handling (Result types)
- Strong typing throughout

## Challenges

### Technical
1. Learning curve: Team needs Rust expertise
2. Model porting: Converting PyTorch models to Rust frameworks
3. Ecosystem maturity: Some NLP tools less mature than Python/Java
4. Debugging: Cross-language debugging complexity

### Organizational
1. Development velocity: Initial slowdown during learning phase
2. Library availability: May need to implement some algorithms from scratch
3. Community support: Smaller NLP community in Rust
4. Maintenance burden: Two codebases during transition

## Risk Mitigation

1. Gradual migration: Keep Java backend available during transition
2. Feature flags: Allow switching between implementations
3. Extensive testing: Automated accuracy and performance tests
4. Fallback strategy: Option to revert to Java if needed
5. Community engagement: Contribute to and leverage Rust NLP ecosystem

## Alternative: Hybrid Approach

Instead of full migration, consider strategic use of Rust:

1. Performance hotspots only
   - Pattern matching (Semgrex/Tokensregex)
   - Graph algorithms
   - Tokenization

2. Keep Java for
   - Complex models not yet in Rust
   - Well-tested existing functionality
   - Features used infrequently

3. Benefits
   - Lower risk
   - Faster time to value
   - Incremental improvement

## Timeline Estimate

- Assessment & Prototyping: 2 months
- Core Infrastructure: 3 months  
- Priority Features: 6 months
- Advanced Features: 4 months
- Testing & Hardening: 3 months
- Total: 18 months to feature parity

## Resources Required

- 2-3 senior Rust engineers (full-time)
- 1-2 NLP researchers (part-time, for model validation)
- DevOps support for build/deployment automation
- Compute resources for benchmarking and testing

## Success Metrics

1. Performance: 2x improvement in throughput
2. Memory: 50% reduction in memory usage
3. Accuracy: <1% degradation vs CoreNLP
4. Deployment: 75% reduction in deployment complexity
5. Startup: <100ms cold start vs >5s for JVM

## References

- [Candle - Minimalist ML framework](https://github.com/huggingface/candle)
- [Burn - Deep Learning Framework](https://github.com/tracel-ai/burn)
- [tokenizers - Fast tokenization](https://github.com/huggingface/tokenizers)
- [rust-bert - BERT in Rust](https://github.com/guillaume-be/rust-bert)
- [PyO3 - Rust-Python bindings](https://pyo3.rs/)
- [Linfa - ML framework](https://github.com/rust-ml/linfa)
- [tantivy - Full-text search](https://github.com/quickwit-oss/tantivy)

## Next Steps

1. Form evaluation team
2. Set up Rust development environment
3. Build minimal PyO3 proof-of-concept
4. Benchmark critical path: tokenization
5. Present findings and get go/no-go decision
