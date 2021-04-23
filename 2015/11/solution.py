import sys
import re
from string import ascii_lowercase as alphabet

INPUT = "vzbxkghb"
LEN_ALPHABET = len(alphabet)
# Note we are assuming that 'z' is not a bad char
BAD_CHARS = "iol"
PASSWORD_LENGTH = 8
NEXT_CHAR_DICT = dict(zip(alphabet, alphabet[1:]))

PAIR_OF_PAIRS_PATTERN = re.compile(r"\w*(\w)(\1)\w*(?!1)(\w)(\3)\w*")

ASCENDING_CHAR_TRIPLES = [
    a + b + c for a, b, c in zip(alphabet, alphabet[1:], alphabet[2:])
]


def check_password(string: str) -> bool:
    cond1 = all(e not in string for e in BAD_CHARS)
    cond2 = bool(PAIR_OF_PAIRS_PATTERN.match(string))
    cond3 = any(t in string for t in ASCENDING_CHAR_TRIPLES)

    return all([cond1, cond2, cond3])


def increment(string: str) -> str:
    for i, e in enumerate(string):
        if e in BAD_CHARS:
            tail_length = PASSWORD_LENGTH - i - 1
            return string[:i] + NEXT_CHAR_DICT[e] + 'a'*tail_length

    body, tail = string[:-1], string[-1]

    if tail != 'z':
        return body + NEXT_CHAR_DICT[tail]
    else:
        return increment(body) + 'a'


def get_next_good_password(string: str) -> str:
    while len(string) <= PASSWORD_LENGTH:
        if check_password(string):
            return string
        else:
            string = increment(string)
    
    raise ValueError("Unable to find a password of suitable length")


def main(password: str):
    ans = get_next_good_password(password)

    print("New password: {}".format(ans))

    new_ans = get_next_good_password(increment(ans))

    print("New new password: {}".format(new_ans))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = INPUT
    main(password)