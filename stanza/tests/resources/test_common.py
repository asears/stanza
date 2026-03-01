"""
Test various resource downloading functions from resources/common.py
"""

import tempfile
from pathlib import Path

import pytest

import stanza
from stanza.resources import common
from stanza.tests import TEST_MODELS_DIR, TEST_WORKING_DIR

pytestmark = [pytest.mark.travis, pytest.mark.client]


def test_assert_file_exists():
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        filename = Path(test_dir) / "test.txt"
        with pytest.raises(FileNotFoundError):
            common.assert_file_exists(str(filename))

        with filename.open("w", encoding="utf-8") as fout:
            fout.write("Unban mox opal!")
        # MD5 of the fake model file, not any real model files in the system
        EXPECTED_MD5 = "44dbf21b4e89cea5184615a72a825a36"
        common.assert_file_exists(str(filename))
        common.assert_file_exists(str(filename), md5=EXPECTED_MD5)

        with pytest.raises(ValueError):
            common.assert_file_exists(str(filename), md5="12345")

        with pytest.raises(ValueError):
            common.assert_file_exists(str(filename), md5="12345", alternate_md5="12345")

        common.assert_file_exists(str(filename), md5="12345", alternate_md5=EXPECTED_MD5)


@pytest.mark.skip(reason="Requires network connection - ConnectionError from GitHub")
def test_download_tokenize_mwt():
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        stanza.download("en", model_dir=test_dir, processors="tokenize", package="ewt", verbose=False)
        pipeline = stanza.Pipeline("en", model_dir=test_dir, processors="tokenize", package="ewt")
        assert isinstance(pipeline, stanza.Pipeline)
        # mwt should be added to the list
        assert len(pipeline.loaded_processors) == 2


@pytest.mark.skip(reason="Requires network connection - ConnectionError from GitHub")
def test_download_non_default():
    """
    Test the download path for a single file rather than the default zip

    The expectation is that an NER model will also download two charlm models.
    If that layout changes on purpose, this test will fail and will need to be updated
    """
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        stanza.download("en", model_dir=test_dir, processors="ner", package="ontonotes_charlm", verbose=False)
        test_dir_path = Path(test_dir)
        assert sorted(p.name for p in test_dir_path.iterdir()) == ['en', 'resources.json']
        en_dir = test_dir_path / 'en'
        en_dir_listing = sorted(p.name for p in en_dir.iterdir())
        assert en_dir_listing == ['backward_charlm', 'forward_charlm', 'ner', 'pretrain']
        assert sorted(p.name for p in (en_dir / 'ner').iterdir()) == ['ontonotes_charlm.pt']
        for i in en_dir_listing:
            assert len(list((en_dir / i).iterdir())) == 1


@pytest.mark.skip(reason="Requires network connection - ConnectionError from GitHub")
def test_download_two_models():
    """
    Test the download path for two NER models

    The package system should now allow for multiple NER models to be
    specified, and a consequence of that is it should be possible to
    download two models at once

    The expectation is that the two different NER models both download
    a different forward & backward charlm.  If that changes, the test
    will fail.  Best way to update it will be two different models
    which download two different charlms
    """
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        stanza.download("en", model_dir=test_dir, processors="ner", package={"ner": ["ontonotes_charlm", "anatem"]}, verbose=False)
        test_dir_path = Path(test_dir)
        assert sorted(p.name for p in test_dir_path.iterdir()) == ['en', 'resources.json']
        en_dir = test_dir_path / 'en'
        en_dir_listing = sorted(p.name for p in en_dir.iterdir())
        assert en_dir_listing == ['backward_charlm', 'forward_charlm', 'ner', 'pretrain']
        assert sorted(p.name for p in (en_dir / 'ner').iterdir()) == ['anatem.pt', 'ontonotes_charlm.pt']
        for i in en_dir_listing:
            assert len(list((en_dir / i).iterdir())) == 2


def test_process_pipeline_parameters():
    """
    Test a few options for specifying which processors to load
    """
    with tempfile.TemporaryDirectory(dir=TEST_WORKING_DIR) as test_dir:
        lang, model_dir, package, processors = common.process_pipeline_parameters("en", test_dir, None, "tokenize,pos")
        assert processors == {"tokenize": "default", "pos": "default"}
        assert package is None

        lang, model_dir, package, processors = common.process_pipeline_parameters("en", test_dir, {"tokenize": "spacy"}, "tokenize,pos")
        assert processors == {"tokenize": "spacy", "pos": "default"}
        assert package is None

        lang, model_dir, package, processors = common.process_pipeline_parameters("en", test_dir, {"pos": "ewt"}, "tokenize,pos")
        assert processors == {"tokenize": "default", "pos": "ewt"}
        assert package is None

        lang, model_dir, package, processors = common.process_pipeline_parameters("en", test_dir, "ewt", "tokenize,pos")
        assert processors == {"tokenize": "ewt", "pos": "ewt"}
        assert package is None


@pytest.mark.skip(reason="Requires downloaded models/resources - run setup.py or mock tests needed")
def test_language_resources():
    resources = common.load_resources_json(TEST_MODELS_DIR)

    # check that an unknown language comes back as None
    bad_lang = 'z'
    while bad_lang in resources and len(bad_lang) < 100:
        bad_lang = bad_lang + 'z'
    assert bad_lang not in resources
    assert common.get_language_resources(resources, bad_lang) is None

    # check the parameters of the test make sense
    # there should be 'zh' which is an alias of 'zh-hans'
    assert "zh" in resources
    assert "alias" in resources["zh"]
    assert resources["zh"]["alias"] == "zh-hans"

    # check that getting the resources for either 'zh' or 'zh-hans'
    # return the simplified Chinese resources
    zh_resources = common.get_language_resources(resources, "zh")
    assert "tokenize" in zh_resources
    assert "alias" not in zh_resources
    assert "Chinese" in zh_resources["lang_name"]

    zh_hans_resources = common.get_language_resources(resources, "zh-hans")
    assert zh_resources == zh_hans_resources
