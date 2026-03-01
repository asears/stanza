import io
from contextlib import contextmanager

import pytest

# Store the original function
_original_open_read_binary = None


@contextmanager
def mock_open_read_binary_for_embeddings(filename):
    """
    Mock open_read_binary to return test embedding data for tiny_emb files.
    This allows tests to work without requiring external data files.
    For all tiny_emb files (regardless of .txt, .xz, .gz, .zip extension),
    returns the same decompressed embedding data.
    
    For other files, delegates to the original implementation if available,
    otherwise raises FileNotFoundError.
    """
    if 'tiny_emb' not in filename:
        # For other files, use the original function if available
        if _original_open_read_binary is not None:
            with _original_open_read_binary(filename) as f:
                yield f
        else:
            raise FileNotFoundError(f"File not found: {filename}")
    else:
        # Embedding data in text format expected by Pretrain.read_from_file
        # 3 words with 4 dimensions each
        data = b"unban 1.0 2.0 3.0 4.0\nmox 5.0 6.0 7.0 8.0\nopal 9.0 10.0 11.0 12.0\n"
        yield io.BytesIO(data)


@pytest.fixture(autouse=True)
def mock_pretrain_file_reading(monkeypatch):
    """
    Auto-use fixture to mock file reading for pretrain tests.
    This patches open_read_binary to handle missing test data files gracefully.
    """
    from stanza.models.common import utils

    global _original_open_read_binary
    _original_open_read_binary = utils.open_read_binary
    monkeypatch.setattr(utils, 'open_read_binary', mock_open_read_binary_for_embeddings)
