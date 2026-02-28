import sys
import json
from pathlib import Path

def avg_sent_len(toklabels):
    toklabels = Path(toklabels)
    if toklabels.suffix == '.json':
        with toklabels.open() as f:
            l = json.load(f)

        l = [''.join([str(x[1]) for x in para]) for para in l]
    else:
        with toklabels.open() as f:
            l = ''.join(f.readlines())

        l = l.split('\n\n')

    sentlen = [len(x) + 1 for para in l for x in para.split('2')]
    return sum(sentlen) / len(sentlen)

if __name__ == '__main__':
    print(avg_sent_len(sys.args[1]))
