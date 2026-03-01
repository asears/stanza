# Converting `decode_predictions` to a Standalone Rust Function

Rewriting the heavily CPU-bound `decode_predictions` function in Rust can drastically speed up execution. Rust handles loops, string matching, and memory allocations far more efficiently than Python, and natively supports fearless multithreading without a Global Interpreter Lock (GIL).

## Plan for Rust Implementation

### 1. Tooling and Interoperability
- **PyO3**: Use the PyO3 crate to create native Python bindings.
- **Maturin**: Use Maturin to compile and package the Rust code as a standard Python wheel, seamlessly integrating into Stanza's build process.

### 2. Data Structures
Convert Python data inputs (`vocab`, `mwt_dict`, `orig_text`, `all_raw`, `all_preds`) to their nearest Rust equivalents when passing the FFI boundary:
- `orig_text`: `&str`
- `all_raw`: `Vec<Vec<String>>` (or potentially `Vec<Vec<char>>` for exact unicode character representation).
- `all_preds`: `Vec<Vec<i32>>`
- Returns: Tuple natively serialized back to Python `(oov_count, total_offset, doc_objects_list)`.

### 3. Implementation Steps
- **Step 1 - Scaffolding**: Initialize a new library crate (e.g., `stanza_rust_tokenizer`) with PyO3 bindings.
- **Step 2 - Map the Core Logic**: Port the double `for` loop that iterates over `zip(raw, pred)` into Rust. Handle the state machines for `current_tok` and `current_sent`.
- **Step 3 - String Indexing Engine**: Rust handles strings and slices in UTF-8 byte arrays safely. Careful translation from Python's character-based offset (`char_offset`) to Rust's byte-index boundaries (e.g. using `.char_indices()`) will be crucial to avoid panics and misalignment.
- **Step 4 - Regex Compatibility**: Bring in the `regex` crate in Rust. Precompile required regexes at the module level utilizing `lazy_static` or `OnceCell`.
- **Step 5 - Parallel Processing (`rayon`)**: Replace the outermost sequential loops over `all_raw` and `all_preds` with `.into_par_iter()` from the `rayon` crate. Paragraph offsets can be pre-calculated in a swift localized string search to isolate the state across threads.

### 4. Integration
Update `utils.py` in Stanza to fallback gracefully:
```python
try:
    from stanza_rust_tokenizer import decode_predictions_rust
    decode_predictions = decode_predictions_rust
except ImportError:
    # Print warning optionally
    # Fallback to pure Python decode_predictions
    pass
```
This isolates the dependency and ensures Stanza continues to operate even on architectures where the compiled Rust binaries aren't available upfront.