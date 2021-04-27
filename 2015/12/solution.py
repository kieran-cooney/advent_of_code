import sys
import json
from typing import Union

Json = Union[list, dict, int, str]


def sum_json(d: Json, ignore_red: bool=False) -> int:
    b = ignore_red

    if isinstance(d, int):
        return d

    elif isinstance(d, str):
        return 0

    elif isinstance(d, dict):
        if b and ('red' in d.values()):
            return 0
        else:
            return sum(sum_json(k, b) + sum_json(v, b) for k, v in d.items())

    elif isinstance(d, list):
        return sum(sum_json(e, b) for e in d)

    else:
        raise ValueError('Argument type {} is invalid'.format(type(d)))


def main(filepath: str) -> None:
    with open("input.txt", "r") as f:
        data = json.load(f)
    
    ans1 = sum_json(data)
    ans2 = sum_json(data, True)

    print("Answer for part 1: {}".format(ans1))
    print("Answer for part 2: {}".format(ans2))


if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"
    main(filepath)