"""
Basic tests of the stanza data objects, especially the setter/getter routines
"""
import pytest

import stanza
from stanza.models.common.doc import ID, TEXT, Document, Sentence, Word
from stanza.tests import *

pytestmark = pytest.mark.pipeline

# data for testing
EN_DOC = "This is a test document. Pretty cool!"

EN_DOC_UPOS_XPOS = (('PRON_DT', 'AUX_VBZ', 'DET_DT', 'NOUN_NN', 'NOUN_NN', 'PUNCT_.'), ('ADV_RB', 'ADJ_JJ', 'PUNCT_.'))

EN_DOC2 = "Chris Manning wrote a sentence. Then another."


@pytest.fixture(scope="module")
def nlp_pipeline():
    nlp = stanza.Pipeline(dir=str(TEST_MODELS_DIR), lang='en', download_method=None)
    return nlp


@pytest.mark.skip(reason="TODO: avoid network/resource fetch dependency for readonly pipeline test")
def test_readonly(nlp_pipeline):
    Document.add_property('some_property', 123)
    doc = nlp_pipeline(EN_DOC)
    assert doc.some_property == 123
    with pytest.raises(ValueError):
        doc.some_property = 456


def test_readonly_mocked(mocker):
    """
    Test readonly custom property behavior without pipeline/network access.
    """
    Document.add_property('some_property_mocked', 123)
    mock_doc = Document([[{ID: 1, TEXT: "This"}]])
    mock_pipeline = mocker.Mock(return_value=mock_doc)

    doc = mock_pipeline(EN_DOC)
    assert doc.some_property_mocked == 123
    with pytest.raises(ValueError):
        doc.some_property_mocked = 456

    mock_pipeline.assert_called_once_with(EN_DOC)


@pytest.mark.skip(reason="TODO: avoid network/resource fetch dependency for getter pipeline test")
def test_getter(nlp_pipeline):
    Word.add_property('upos_xpos', getter=lambda self: f"{self.upos}_{self.xpos}")

    doc = nlp_pipeline(EN_DOC)

    assert tuple(tuple(word.upos_xpos for word in sentence.words) for sentence in doc.sentences) == EN_DOC_UPOS_XPOS


def test_getter_mocked():
    """
    Test Word getter property behavior without pipeline/network access.
    """
    Word.add_property('upos_xpos_mocked', getter=lambda self: f"{self.upos}_{self.xpos}")
    doc = Document([[{ID: 1, TEXT: "This", "upos": "PRON", "xpos": "DT"},
                     {ID: 2, TEXT: "is", "upos": "AUX", "xpos": "VBZ"}]])
    assert tuple(word.upos_xpos_mocked for word in doc.sentences[0].words) == ('PRON_DT', 'AUX_VBZ')


@pytest.mark.skip(reason="TODO: avoid network/resource fetch dependency for setter/getter pipeline test")
def test_setter_getter(nlp_pipeline):
    int2str = {0: 'ok', 1: 'good', 2: 'bad'}
    str2int = {'ok': 0, 'good': 1, 'bad': 2}

    def setter(self, value):
        self._classname = str2int[value]
    Sentence.add_property('classname', getter=lambda self: int2str[self._classname] if self._classname is not None else None, setter=setter)

    doc = nlp_pipeline(EN_DOC)
    sentence = doc.sentences[0]
    sentence.classname = 'good'
    assert sentence._classname == 1

    # don't try this at home
    sentence._classname = 2
    assert sentence.classname == 'bad'


def test_setter_getter_mocked():
    """
    Test Sentence setter/getter property behavior without pipeline/network access.
    """
    int2str = {0: 'ok', 1: 'good', 2: 'bad'}
    str2int = {'ok': 0, 'good': 1, 'bad': 2}

    def setter(self, value):
        self._classname = str2int[value]

    Sentence.add_property('classname_mocked', getter=lambda self: int2str[self._classname] if self._classname is not None else None, setter=setter)

    doc = Document([[{ID: 1, TEXT: "This"}]])
    sentence = doc.sentences[0]
    sentence.classname_mocked = 'good'
    assert sentence._classname == 1

    sentence._classname = 2
    assert sentence.classname_mocked == 'bad'


@pytest.mark.skip(reason="TODO: avoid network/resource fetch dependency for backpointer pipeline test")
def test_backpointer(nlp_pipeline):
    doc = nlp_pipeline(EN_DOC2)
    ent = doc.ents[0]
    assert ent.sent is doc.sentences[0]
    assert list(doc.iter_words())[0].sent is doc.sentences[0]
    assert list(doc.iter_tokens())[-1].sent is doc.sentences[-1]


def test_backpointer_mocked():
    """
    Test word/token sentence backpointers without pipeline/network access.
    """
    doc = Document([
        [{ID: 1, TEXT: "Chris"}, {ID: 2, TEXT: "Manning"}],
        [{ID: 3, TEXT: "wrote"}, {ID: 4, TEXT: "another"}],
    ])

    assert list(doc.iter_words())[0].sent is doc.sentences[0]
    assert list(doc.iter_tokens())[-1].sent is doc.sentences[-1]
