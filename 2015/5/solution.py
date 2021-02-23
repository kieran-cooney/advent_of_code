import sys
import re
from operator import add
from functools import reduce

from typing import List, Iterable, Pattern

# Regex is type representing a compiled regex.
Regex = Pattern[str]
Regexes = Iterable[Pattern[str]]

# List of lists for parts 1 and 2
REGEX_PATTERNS = [
    [r"([aeiou].*){3}", r"([a-z])\1{1}", r"^((?!ab|cd|pq|xy).)*$"],
    [r"([a-z]{2}).*\1", r"([a-z])[a-z]\1"]
]

def read_input(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.strip()


def regexp_match(string: str, regex: Regex) -> bool:
    return bool(regex.search(string))


def good_string(string: str, regexes: Regexes,
                verbose: bool = False) -> bool:
    """Checks if string matches against each regex in regexes"""
    results = [regexp_match(string, r) for r in regexes]

    result = all(results)

    if verbose:
        print("Results for {}".format(string))
        print("Sub tests: {}".format(results))
        print("Final result: {}".format(result))

    return result


def count_good_strings(strings: Iterable[str],
                        regex_lists: List[Regexes],
                        verbose: bool=False) -> List[int]:
    """
    Checks how many of strings match and returns a list of these counts for
    each list of regexes in regex_lists
    """
    def list_sum(l1, l2):
        """
        Helper function to add two lists pair-wise
        returning a list of the same length
        """
        return map(add, l1, l2)

    # Iterator of lists of good_string results for each regex_list
    good_strings = (
        [good_string(s, r, verbose) for r in regex_lists]
        for s in strings
    )

    return reduce(list_sum, good_strings)


def main(filepath: str):
    strings = read_input(filepath)

    # Compile regexes here so we only have to do it once.
    compiled_regexes = [[re.compile(s) for s in l ] for l in REGEX_PATTERNS]

    num_good_strings = count_good_strings(strings, compiled_regexes)

    for i, ans in enumerate(num_good_strings, start=1):
        print("Part {}: {} good strings found".format(i, ans))


if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'
    main(filepath)
