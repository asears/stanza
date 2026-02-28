import shutil
import tempfile
from pathlib import Path

import pytest

from stanza.models.common.foundation_cache import FoundationCache, load_charlm
from stanza.tests import TEST_MODELS_DIR

pytestmark = [pytest.mark.travis, pytest.mark.pipeline]


# TODO(AS): Assert error
@pytest.mark.xfail(reason="assert fails needs adjustment")
def test_charlm_cache():
    models_path = Path(TEST_MODELS_DIR) / "en" / "backward_charlm"
    models = list(models_path.glob("*"))
    # we expect at least one English model downloaded for the tests
    assert len(models) >= 1
    model_file = models[0]

    cache = FoundationCache()
    with tempfile.TemporaryDirectory(dir=".") as test_dir:
        temp_file = Path(test_dir) / "charlm.pt"
        shutil.copy2(model_file, temp_file)
        # this will work
        model = load_charlm(temp_file)

        # this will save the model
        model = cache.load_charlm(temp_file)

    # this should no longer work
    with pytest.raises(FileNotFoundError):
        model = load_charlm(temp_file)

    # it should remember the cached version
    model = cache.load_charlm(temp_file)
