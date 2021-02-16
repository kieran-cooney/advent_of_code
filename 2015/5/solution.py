
import sys
import re

from typing import List, Iterable

VOWELS = 'aeiou'
# Regex to check for repeated character
REPEATED_CHAR_PATTERN = re.compile(r"([a-z])\1{1}")
BAD_STRINGS = ['ab', 'cd', 'pq', 'xy']


def read_input(filepath: str) => Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.strip()


def contains_vowels(string: str, num_vowels: int =3) -> bool:
    string_vowels = [e for e in string if e in VOWELS]
    return (len(string_vowels) >= num_vowels)


def contains_repeated_char(string: str) -> bool:
    return bool(REPEATED_CHAR_PATTERN.search(string))


def contains_bad_string(
    string: str,
    bad_strings: List[str] = BAD_STRINGS) -> bool:
    return any(s in string for s in bad_strings)


def good_string(string: str, verbose: bool = False) -> bool:
    test_results = [
        contains_vowels(string),
        contains_repeated_char(string),
        not contains_bad_string(string)
    ]

    result = all(test_results)

    if verbose:
        print("Results for {}".format(string))
        print("Sub tests: {}".format(test_results))
        print("Final result: {}".format(result))

    return result


def count_good_strings(strings: Iterable[str]) -> int:
    return sum(1 for s in strings if good_string(s))


def main(filepath: str):
    strings = read_input(filepath)
    num_good_strings = count_good_strings(strings)
    print("Part 1: {} good strings found".format(num_good_strings))


if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'
    main(filepath)
