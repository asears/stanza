"""
Test installation functions.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

import stanza
from stanza.tests import TEST_WORKING_DIR

pytestmark = [pytest.mark.travis, pytest.mark.client]


def test_install_corenlp():
    # we do not reset the CORENLP_HOME variable since this may impact the
    # client tests
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:

        # the download method doesn't install over existing directories
        shutil.rmtree(test_dir)
        stanza.install_corenlp(dir=test_dir)

        test_dir_path = Path(test_dir)
        assert test_dir_path.is_dir(), "Installation destination directory not found."
        jar_files = [f for f in test_dir_path.iterdir()
                     if f.name.endswith('.jar') and f.name.startswith('stanford-corenlp')]
        assert len(jar_files) > 0, \
            "Cannot find stanford-corenlp jar files in the installation directory."
        assert not (test_dir_path / 'corenlp.zip').exists(), \
            "Downloaded zip file was not removed."


def test_download_corenlp_models():
    model_name = "arabic"
    version = "4.2.2"

    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        stanza.download_corenlp_models(model=model_name, version=version, dir=test_dir)

        dest_file = Path(test_dir) / f"stanford-corenlp-{version}-models-{model_name}.jar"
        assert dest_file.is_file(), "Downloaded model file not found."


def test_download_tokenize_mwt():
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        stanza.download("en", model_dir=test_dir, processors="tokenize", package="ewt", verbose=False)
        pipeline = stanza.Pipeline("en", model_dir=test_dir, processors="tokenize", package="ewt")
        assert isinstance(pipeline, stanza.Pipeline)
        # mwt should be added to the list
        assert len(pipeline.loaded_processors) == 2
