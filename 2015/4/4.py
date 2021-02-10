"""
Couldn't get type hints working on this version of python :/
Lists, Dict type hints not woring. Version = 3.6.8
"""
import sys

from hashlib import md5
from pathlib import Path

# Number of possibe values to check.
# Used to prevent the script stalling if no keys found
STOPPING_NUMBER = 10**7


def read_input(filepath):
    """
    Read input from filepath and return cleaned string.
    """
    input = Path(filepath).read_text().strip()
    print("Input string - " + input)
    return input


def get_md5_hash(s):
    """
    Return hexadecimal MD5 hash of input string.
    """
    return md5(s.encode("utf-8")).hexdigest()


def get_advent_coins(input_string, pre_strings):
    """
    Given the secret key input_string, and a list pre_strings, return a
    dictionary with keys from pre_strings and values as (int, str) pairs.
    The int i is the lowest positive integer such that input_string appended
    with i results in a hash key starting with the key pre_string. The str
    in the pair is that same hash key.
    """
    output_dict = dict()
    # Copy pre_strings so we can still use it later. #functional
    pre_strings = pre_strings.copy()

    for i in range(1, STOPPING_NUMBER):
        appended_key = input_string + str(i)
        output_hash = get_md5_hash(appended_key)

        # Add i and output_hash to dict if output_hash is valid
        for pre_string in pre_strings:
            if output_hash.startswith(pre_string):
                output_dict[pre_string] = (i, output_hash)
                pre_strings.remove(pre_string)

        # If we are out of pre_strings to check, then break the for loop.
        if not pre_strings:
            break

    return output_dict


def print_advent_coin(advent_coins_dict, pre_string):
    i, output_hash = advent_coins_dict[pre_string]

    print("Answers for pre_string {}".format(pre_string))
    print("First Advent coin:  {}".format(i))
    print("Associated hash key:  {}".format(output_hash))
    

def main(filepath):
    input_string = read_input(filepath)

    pre_strings = ["0"*5, "0"*6]
    advent_coins_dict = get_advent_coins(input_string, pre_strings)

    for part_number, pre_string in enumerate(pre_strings, start=1):
        print("Part {}:".format(part_number))
        print_advent_coin(advent_coins_dict, pre_string)


if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'
    main(filepath)