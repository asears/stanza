# Performance Improvements for `decode_predictions` in Python

The `decode_predictions` function in `stanza/models/tokenization/utils.py` processes raw characters and predicts token/sentence boundaries sequentially. Because it heavily relies on character-by-character string concatenation, regex operations, and string index lookups, it can be a significant CPU bottleneck.

## Strategies for Improvement

### 1. Optimize Character Collection & Concatenation
Currently, the function uses string concatenation within a loop (`current_tok += t`), which creates new string objects continuously.
- **Improvement:** Track start and end indices of the tokens within the `raw` sequence. Only extract the slice (e.g., `"".join(raw[start:end])`) when an end-of-token condition is met (`p >= 1`).

### 2. Pre-compile or Cache Regular Expressions
In the loop, `part_pattern = re.compile(r'\s*'.join(re.escape(c) for c in part))` is compiled on the fly for every single token part when `skip_newline` is enabled.
- **Improvement:** Use `functools.lru_cache` to memoize the regex compilation step, as the character combinations and tokens are often repeated. Alternatively, re-evaluate if the regex is strictly necessary or if string slicing with standard find/index can be used.

### 3. Leverage `itertools`
The function currently manages states like `current_tok` and `current_sent` manually during the character loop.
- **Improvement:** Use `itertools.groupby` to group characters by their prediction label (e.g., grouping `p == 0` characters together) to construct tokens in bulk instead of character by character.

### 4. Parallelism (Process-based)
Because Python's Global Interpreter Lock (GIL) restricts thread-based parallelism for CPU-bound tasks, we can utilize `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.
- **Strategy:** `all_raw` and `all_preds` are lists of sequences, usually representing paragraphs or documents. Each sequence can be decoded independently.
- **Challenge:** The `char_offset` mechanism accumulates linearly across the entire loop to match subsets against `orig_text`.
- **Solution:** 
  1. Pre-calculate the starting `char_offset` for each paragraph/sequence by finding sequence boundaries in `orig_text` beforehand.
  2. Map the localized decoding function over each `(raw_seq, pred_seq, start_char_offset)` tuple using `ProcessPoolExecutor.map`.
  3. Reduce and concatenate the parsed `doc` lists and linearly sum up the `oov_count`.