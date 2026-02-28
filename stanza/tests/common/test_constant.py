"""
Test the conversion to lcodes and splitting of dataset names
"""


import pytest

from stanza.models.common.constant import (
    is_right_to_left,
    lang_to_langcode,
    langlower2lcode,
    treebank_to_short_name,
    two_to_three_letters,
)
from stanza.tests import *

pytestmark = [pytest.mark.travis, pytest.mark.pipeline]


def test_treebank():
    """
    Test the entire treebank name conversion
    """
    # conversion of a UD_ name
    assert treebank_to_short_name("UD_Hindi-HDTB") == "hi_hdtb"
    # conversion of names without UD
    assert treebank_to_short_name("Hindi-fire2013") == "hi_fire2013"
    assert treebank_to_short_name("Hindi-Fire2013") == "hi_fire2013"
    assert treebank_to_short_name("Hindi-FIRE2013") == "hi_fire2013"
    # already short names are generally preserved
    assert treebank_to_short_name("hi-fire2013") == "hi_fire2013"
    assert treebank_to_short_name("hi_fire2013") == "hi_fire2013"
    # a special case
    assert treebank_to_short_name("UD_Chinese-PUD") == "zh-hant_pud"
    # a special case already converted once
    assert treebank_to_short_name("zh-hant_pud") == "zh-hant_pud"
    assert treebank_to_short_name("zh-hant-pud") == "zh-hant_pud"
    assert treebank_to_short_name("zh-hans_gsdsimp") == "zh-hans_gsdsimp"

    assert treebank_to_short_name("wo_masakhane") == "wo_masakhane"
    assert treebank_to_short_name("wol_masakhane") == "wo_masakhane"
    assert treebank_to_short_name("Wol_masakhane") == "wo_masakhane"
    assert treebank_to_short_name("wolof_masakhane") == "wo_masakhane"
    assert treebank_to_short_name("Wolof_masakhane") == "wo_masakhane"


def test_lang_to_langcode():
    assert lang_to_langcode("Hindi") == "hi"
    assert lang_to_langcode("HINDI") == "hi"
    assert lang_to_langcode("hindi") == "hi"
    assert lang_to_langcode("HI") == "hi"
    assert lang_to_langcode("hi") == "hi"


def test_right_to_left():
    assert is_right_to_left("ar")
    assert is_right_to_left("Arabic")

    assert not is_right_to_left("en")
    assert not is_right_to_left("English")


def test_two_to_three():
    assert lang_to_langcode("Wolof") == "wo"
    assert lang_to_langcode("wol") == "wo"

    assert "wo" in two_to_three_letters
    assert two_to_three_letters["wo"] == "wol"


def test_langlower():
    assert lang_to_langcode("WOLOF") == "wo"
    assert lang_to_langcode("nOrWeGiAn") == "nb"

    assert langlower2lcode["soi"] == "soj"
    assert langlower2lcode["sohi"] == "soj"
