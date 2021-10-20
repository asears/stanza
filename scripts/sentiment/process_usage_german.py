"""
USAGE is produced by the same people as SCARE.

Dataset:

https://www.romanklinger.de/usagecorpus/

Notes:

USAGE has a German and English part.  This script parses the German part.

Path should be where USAGE was unpacked.  It will have the
documents, files, etc subdirectories.

Example:

  process_usage_german.py path

"""

import csv
import glob
import os
import sys

import stanza

import scripts.sentiment.process_utils as process_utils

basedir = sys.argv[1]
nlp = stanza.Pipeline('de', processors='tokenize')

num_short_items = 0
snippets = []
csv_files = glob.glob(os.path.join(basedir, "files/de*csv"))
for csv_filename in csv_files:
    with open(csv_filename, newline='') as fin:
        cin = csv.reader(fin, delimiter='\t', quotechar=None)
        lines = list(cin)

        for index, line in enumerate(lines):
            begin, end, snippet, sentiment = [line[i] for i in [2, 3, 4, 6]]
            begin_idx = int(begin)
            end_idx = int(end)
            if len(snippet) != end_idx - begin_idx:
                raise ValueError(
                    "Error found in {0} line {1}.  Expected {2} got {3}".format(
                        csv_filename, index, (end_idx - begin_idx), len(snippet)
                    )
                )
            if sentiment.lower() == 'unknown':
                continue
            elif sentiment.lower() == 'positive':
                sentiment = 2
            elif sentiment.lower() == 'neutral':
                sentiment = 1
            elif sentiment.lower() == 'negative':
                sentiment = 0
            else:
                raise ValueError("Tell John he screwed up and this is why he can't have Mox Opal: {0}".format(sentiment))
            doc = nlp(snippet)
            text = " ".join(" ".join(token.text for token in sentence.tokens) for sentence in doc.sentences)
            num_tokens = sum(len(sentence.tokens) for sentence in doc.sentences)
            if num_tokens < 4:
                num_short_items = num_short_items + 1
            snippets.append("%d %s" % (sentiment, text))


print(len(snippets))

process_utils.write_list(os.path.join(basedir, "de-train.txt"), snippets)
