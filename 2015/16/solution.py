import re
import numpy as np
from collections import Counter

LINE_PATTERN = re.compile(r"^Sue (\d+): (.*)$")

GIFT_COMPOUNDS = [
    ('children', 3),
    ('cats', 7),
    ('samoyeds', 2),
    ('pomeranians', 3),
    ('akitas', 0),
    ('vizslas', 0),
    ('goldfish', 5),
    ('trees', 3),
    ('cars', 2),
    ('perfumes', 1)
]

compound_indices = {c: i for i, (c, _) in enumerate(GIFT_COMPOUNDS)}


def parse_compounds(text):
    compound_quantity_strings = text.split(', ')
    compound_quantity_pairs = [
        t.split(': ') for t in compound_quantity_strings
    ]

    return compound_quantity_pairs


def parse_line(line, compound_indices=compound_indices):
    number, compounds = LINE_PATTERN.match(line).groups()
    compound_pairs = parse_compounds(compounds)

    return number, compound_pairs


def parse_input(filepath='input.txt', compound_indices=compound_indices):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    compound_array = np.empty((len(lines), len(compound_indices)))
    compound_array.fill(np.nan)

    number_array = np.zeros(len(lines))

    for i, line in enumerate(lines):
        number, pairs = parse_line(line, compound_indices)
        number_array[i] = int(number)
        for compound, value in pairs:
            compound_array[i, compound_indices[compound]] = int(value)
    
    return number_array, compound_array


def find_sue_indices(compound_array, gift_compounds=GIFT_COMPOUNDS,
                    compound_indices=compound_indices):
    gift_array = np.zeros(len(gift_compounds))
    for c, n in gift_compounds:
        gift_array[compound_indices[c]] = n
    
    equal_amounts = (compound_array == gift_array)
    unknown = np.isnan(compound_array)
    equal_or_unknown = equal_amounts | unknown

    possible_sues = equal_or_unknown.all(axis=1)

    possible_sue_indices = [i for i, b in enumerate(possible_sues) if b]

    return possible_sue_indices


def main():
    number_array, compound_array = parse_input()
    sue_indices = find_sue_indices(compound_array)

    print("Number of possible sues found: {}".format(len(sue_indices)))

    print(
        "The numbers of the sues found:{}"
        .format(number_array[sue_indices].astype('int'))
    )


if __name__=='__main__':
    main()