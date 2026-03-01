import json
from pathlib import Path

import numpy as np
import pytest

from stanza.models.common import pretrain
from stanza.tests.classifiers.test_data import DATASET, DATASET_WITH_TREES, SENTENCES

EMB_DIM = 5


@pytest.fixture(scope="module")
def fake_embeddings(tmp_path_factory):
    """
    will return a path to a fake embeddings file with the words in SENTENCES
    """
    # could set np random seed here
    words = sorted(set([x.lower() for y in SENTENCES for x in y]))
    words = words[:-1]
    embedding_dir = tmp_path_factory.mktemp("data")
    embedding_txt = embedding_dir / "embedding.txt"
    embedding_pt = embedding_dir / "embedding.pt"
    embedding = np.random.random((len(words), EMB_DIM))

    with embedding_txt.open("w", encoding="utf-8") as fout:
        for word, emb in zip(words, embedding):
            fout.write(word)
            fout.write("\t")
            fout.write("\t".join(str(x) for x in emb))
            fout.write("\n")

    pt = pretrain.Pretrain(str(embedding_pt), str(embedding_txt))
    pt.load()
    assert Path(embedding_pt).exists()
    return embedding_pt


@pytest.fixture(scope="module")
def train_file_with_trees(tmp_path_factory):
    """Returns a path to a training file with the same sentences as DATASET but with trees included.

    This is for testing that the training can handle trees in the input.
    """
    train_set = DATASET_WITH_TREES * 20
    train_filename = tmp_path_factory.mktemp("data") / "train_trees.json"
    with train_filename.open("w", encoding="utf-8") as fout:
        json.dump(train_set, fout, ensure_ascii=False)
    return train_filename


@pytest.fixture(scope="module")
def dev_file_with_trees(tmp_path_factory):
    """Returns a path to a dev file with the same sentences as DATASET but with trees included."""
    dev_set = DATASET_WITH_TREES * 2
    dev_filename = tmp_path_factory.mktemp("data") / "dev_trees.json"
    with dev_filename.open("w", encoding="utf-8") as fout:
        json.dump(dev_set, fout, ensure_ascii=False)
    return dev_filename


@pytest.fixture(scope="module")
def train_file(tmp_path_factory):
    """Returns a path to a training file with the same sentences as DATASET but without trees included."""
    train_set = DATASET * 20
    train_filename = tmp_path_factory.mktemp("data") / "train.json"
    with train_filename.open("w", encoding="utf-8") as fout:
        json.dump(train_set, fout, ensure_ascii=False)
    return train_filename


@pytest.fixture(scope="module")
def dev_file(tmp_path_factory):
    """Returns a path to a dev file with the same sentences as DATASET but without trees included."""
    dev_set = DATASET * 2
    dev_filename = tmp_path_factory.mktemp("data") / "dev.json"
    with dev_filename.open("w", encoding="utf-8") as fout:
        json.dump(dev_set, fout, ensure_ascii=False)
    return dev_filename


@pytest.fixture(scope="module")
def test_file(tmp_path_factory):
    """Returns a path to a test file with the same sentences as DATASET but without trees included."""
    test_set = DATASET
    test_filename = tmp_path_factory.mktemp("data") / "test.json"
    with test_filename.open("w", encoding="utf-8") as fout:
        json.dump(test_set, fout, ensure_ascii=False)
    return test_filename
