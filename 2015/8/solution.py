import re
import sys
import operator
from functools import reduce

from typing import Iterable, Tuple

ESCAPE_CHARS_PATTERN = re.compile(r"(\\\"|\\\\|\\x[0-9a-f][0-9a-f])")


def tuple_add(t1, t2):
    return tuple(map(operator.add, t1, t2))


def load_file(filepath: str) -> Iterable:
        with open(filepath) as f:
            for line in f:
                yield line.strip()


def num_chars_decoded(s: str) -> int:
    return len(re.sub(ESCAPE_CHARS_PATTERN, "|", s)) - 2


def added_chars_encoded(s: str) -> int:
    return sum(1 for e in s if e in r'"\\') + 2


def get_char_differences(len_triple: Tuple[int, int, int]) -> Tuple[int, int]:
    l, l_decoded, d_encoded = len_triple
    return (l - l_decoded, d_encoded)


def main(filepath):
    lines = load_file(filepath)

    length_triples = (
        (len(l), num_chars_decoded(l), added_chars_encoded(l))
        for l in lines
    )

    total_lengths = reduce(tuple_add, length_triples)

    answers = get_char_differences(total_lengths)

    for i, ans in enumerate(answers):
        print("Answer for part {}: {}".format(i, ans))


if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'
    main(filepath)
