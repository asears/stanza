"""
A small dataset of 1500 positive and 1500 negative sentences.
Supposedly has no neutral sentences by design

Dataset:

https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences

https://archive.ics.uci.edu/ml/machine-learning-databases/00331/

License:

See the existing readme for citation requirements etc

Notes:

Files used in the dataset.

amazon_cells_labelled.txt
imdb_labelled.txt
yelp_labelled.txt

Files in the slsd repo were one line per annotation, with labels 0
for negative and 1 for positive.  No neutral labels existed.

Accordingly, we rearrange the text and adjust the label to fit the
0/1/2 paradigm.  Text is retokenized using PTBTokenizer.

<class> <sentence>

This makes a system call to java edu.stanford.nlp.process.PTBTokenizer for tokenization.

Example:

process_slsd.py ./base_dir out_file.txt

"""

import os
import sys
import tempfile
from typing import List

directory = sys.argv[1]
in_filenames = [
    os.path.join(directory, 'amazon_cells_labelled.txt'),
    os.path.join(directory, 'imdb_labelled.txt'),
    os.path.join(directory, 'yelp_labelled.txt'),
]
out_filename = sys.argv[2]

lines: List[str] = []
for filename in in_filenames:
    lines.extend(open(filename, newline=''))

tmp_filename = tempfile.NamedTemporaryFile(delete=False).name
with open(tmp_filename, "w") as fout:
    for line in lines:
        line = line.strip()
        sentiment = line[-1]
        utterance = line[:-1]
        utterance = utterance.replace("!.", "!")
        utterance = utterance.replace("?.", "?")
        if sentiment == '0':
            sentiment = '0'
        elif sentiment == '1':
            sentiment = '2'
        else:
            raise ValueError("Unknown sentiment: {0}".format(sentiment))
        fout.write("%s %s\n" % (sentiment, utterance))


os.system("java edu.stanford.nlp.process.PTBTokenizer -preserveLines %s > %s" % (tmp_filename, out_filename))
os.unlink(tmp_filename)
