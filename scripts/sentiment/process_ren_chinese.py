"""
This processes a Chinese corpus.

Dataset (URL is stale):

http://a1-www.is.tokushima-u.ac.jp/member/ren/Ren-CECps1.0/Ren-CECps1.0.html

https://aclanthology.org/C10-1104.pdf

License:

The authors want a signed document saying you won't redistribute the corpus.

Notes:

The corpus format is a bunch of .xml files, with sentences labeled with various emotions and an overall polarity.  Polarity is labeled as follows:

消极: negative
中性: neutral
积极: positive

Example:

python3 process_ren_chinese.py ./xml_data_dir ./out

"""

import glob
import random
import sys

import xml.etree.ElementTree as ET  # noqa: N814

from collections import namedtuple
from typing import List

import stanza

import scripts.sentiment.process_utils as process_utils

Fragment = namedtuple('Fragment', ['sentiment', 'text'])


def get_phrases(filename) -> List[Fragment]:
    """Get phrases from file."""
    tree = ET.parse(filename)
    fragments = []

    root = tree.getroot()
    for child in root:
        if child.tag == 'paragraph':
            for subchild in child:
                if subchild.tag == 'sentence':
                    text = subchild.attrib['S'].strip()
                    if len(text) <= 2:
                        continue
                    polarity = None
                    for inner in subchild:
                        if inner.tag == 'Polarity':
                            polarity = inner
                            break
                    if polarity is None:
                        print("Found sentence with no polarity in {0}: {1}".format(filename, text))
                        continue
                    if polarity.text == '消极':
                        sentiment = "0"
                    elif polarity.text == '中性':
                        sentiment = "1"
                    elif polarity.text == '积极':
                        sentiment = "2"
                    else:
                        raise ValueError("Unknown polarity {0} in {1}".format(polarity.text, filename))
                    fragments.append(Fragment(sentiment, text))

    return fragments


def main() -> None:
    """Process Ren Chinese corpus."""
    xml_directory = sys.argv[1]
    out_directory = sys.argv[2]
    sentences = []
    for filename in glob.glob(xml_directory + '/xml/cet_*xml'):
        sentences.extend(get_phrases(filename))

    nlp = stanza.Pipeline('zh', processors='tokenize')
    snippets = []
    for sentence in sentences:
        doc = nlp(sentence.text)
        text = " ".join(" ".join(token.text for token in sentence.tokens) for sentence in doc.sentences)
        snippets.append(sentence.sentiment + " " + text)

    print("Found {0} phrases".format(len(snippets)))
    random.seed(1000)
    random.shuffle(snippets)
    process_utils.write_splits(
        out_directory,
        snippets,
        (
            process_utils.Split("train.txt", 0.8),
            process_utils.Split("dev.txt", 0.1),
            process_utils.Split("test.txt", 0.1),
        ),
    )


if __name__ == "__main__":
    main()
