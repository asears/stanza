from argparse import ArgumentParser
from py import process
import pytest
import stanza
from stanza.tests import *

from stanza.utils.datasets.prepare_depparse_treebank import (
    add_specific_args,
    process_treebank
)

pytestmark = [pytest.mark.travis, pytest.mark.pipeline]


def test_add_specific_args():
    """Test add specific args."""
    parser = ArgumentParser()

    add_specific_args(parser=parser)



