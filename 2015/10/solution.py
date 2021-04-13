import sys
from itertools import groupby, chain
from typing import Iterable, List

Sequence = List[int]

INPUT = "1113222113"


def iter_len(iterable: Iterable) -> int:
    return sum(1 for _ in iterable)


def look_and_say(sequence: Sequence) -> Sequence:
    key_group_pairs = groupby(sequence)

    group_length_key_pairs = (
        (iter_len(group), key)
        for key, group in key_group_pairs
    )

    out_sequence = list(chain(*group_length_key_pairs))

    return out_sequence


def repeated_look_and_say(sequence: Sequence, n: int) -> Sequence:
    out_sequence = sequence.copy()

    for i in range(n):
        out_sequence = look_and_say(out_sequence)

    return out_sequence


def main(number_string: str):
    input_sequence = [int(e) for e in number_string]

    ans1 = repeated_look_and_say(input_sequence, 40)
    ans2 = repeated_look_and_say(ans1, 10)

    print("Length of answer 1 : {}".format(len(ans1)))
    print("Length of answer 2 : {}".format(len(ans2)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_string = sys.argv[1]
    else:
        input_string = INPUT
    main(input_string)
