"""
Turns a directory of conllu files from the conll 2017 shared task to a text file

Part of the process for building a charlm dataset

python conll17_to_text.py <directory>

This is an extension of the original script:
  https://github.com/stanfordnlp/stanza-scripts/blob/master/charlm/conll17/conll2txt.py

To build a new charlm for a new language from a conll17 dataset:
- look for conll17 shared task data, possibly here:
  https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1989
- python3 stanza/utils/charlm/conll17_to_text.py ~/extern_data/conll17/Bulgarian --output_directory extern_data/charlm_raw/bg/conll17
- python3 stanza/utils/charlm/make_lm_data.py --langs bg extern_data/charlm_raw extern_data/charlm/
"""

import argparse
import lzma
from pathlib import Path

def process_file(input_filename, output_directory, compress):
    input_filename = Path(input_filename)
    if input_filename.suffix not in ('.conllu', '.xz') or (input_filename.suffix == '.xz' and not str(input_filename).endswith('.conllu.xz')):
        print(f"Skipping {input_filename}")
        return

    if input_filename.suffix == '.xz':
        open_fn = lambda x: lzma.open(x, mode='rt')
        output_filename = Path(str(input_filename)[:-3].replace('.conllu', '.txt'))
    else:
        open_fn = lambda x: x.open()
        output_filename = Path(str(input_filename).replace('.conllu', '.txt'))

    if output_directory:
        output_filename = Path(output_directory) / output_filename.name

    if compress:
        output_filename = Path(str(output_filename) + '.xz')
        output_fn = lambda x: lzma.open(x, mode='wt')
    else:
        output_fn = lambda x: x.open(mode='w')

    if output_filename.exists():
        print("Cowardly refusing to overwrite %s" % output_filename)
        return

    print("Converting %s to %s" % (input_filename, output_filename))
    with open_fn(input_filename) as fin:
        sentences = []
        sentence = []
        for line in fin:
            line = line.strip()
            if len(line) == 0: # new sentence
                sentences.append(sentence)
                sentence = []
                continue
            if line[0] == '#': # comment
                continue
            splitline = line.split('\t')
            assert(len(splitline) == 10) # correct conllu
            id, word = splitline[0], splitline[1]
            if '-' not in id: # not mwt token
                sentence.append(word)

    if sentence:
        sentences.append(sentence)

    print(f"  Read in {len(sentences)} sentences")
    with output_fn(output_filename) as fout:
        fout.write('\n'.join([' '.join(sentence) for sentence in sentences]))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory", help="Root directory with conllu or conllu.xz files.")
    parser.add_argument("--output_directory", default=None, help="Directory to output to.  Will output to input_directory if None")
    parser.add_argument("--no_xz_output", default=True, dest="xz_output", action="store_false", help="Output compressed xz files")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    directory = Path(args.input_directory)
    filenames = sorted(path.name for path in directory.iterdir())
    print(f"Files to process in {directory}: {filenames}")
    print(f"Processing to .xz files: {args.xz_output}")

    if args.output_directory:
        Path(args.output_directory).mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        process_file(directory / filename, args.output_directory, args.xz_output)

