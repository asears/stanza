import sys

import json
from typing import List


def max_mwt_length(filenames: List[str]) -> int:
    """Max MWT length in a list of files."""
    max_len = 0
    for filename in filenames:
        with open(filename) as f:
            d = json.load(f)
            max_len = max([max_len] + [len(" ".join(x[0][1])) for x in d])
    return max_len


if __name__ == '__main__':
    print(max_mwt_length(sys.argv[1:]))
