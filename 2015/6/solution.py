"""
Solution to day 6 of advent of code 2015: https://adventofcode.com/2015/day/6
I use array.array here in place of numpy array. I wouldn't recommend this in
general, but thought it would be interesting to try. array is a library that
comes with python, so there is no installing and little importing involved

Note we are representing a 2-d grid of lights by flattening it into a 1-d array.
The 1000 lights in the first row are first, then the second 1000 directly after,
etc.
"""

import re
import sys

from array import array
from typing import Tuple, Iterable

Instruction = Tuple[str, int, int, int, int]
Lights = Iterable[int]

GRID_WIDTH = 1000

"""
Regex which takes a line like "turn on 0,1 through 2,3" and expands it into
the tuple
("turn on", 0, 1, 2, 3)
"""
REGEX_PARSER = re.compile(
    r"^(.+)\s(\d{1,3}),(\d{1,3})\s\w+\s(\d{1,3}),(\d{1,3})$"
)


def parse_line(s: str) -> Instruction:
    """Parse an instruction line into a 5-tuple using the above regex"""
    r_tuple = REGEX_PARSER.match(s).groups()
    instruction_tuple = (r_tuple[0], ) + tuple(int(i) for i in r_tuple[1:])
    return instruction_tuple


def parse_input(filepath: str) -> Iterable[Instruction]:
    with open(filepath) as f:
        for line in f:
            yield parse_line(line.strip())


def update_light(lights: Lights, instruction_type: str, lights_index: int):
    """
    Update a the light of lights at light_index according to instruction type
    """
    if instruction_type == 'turn on':
        lights[lights_index] = 1
    elif instruction_type == 'turn off':
        lights[lights_index] = 0
    elif instruction_type == 'toggle':
        lights[lights_index] = 1 - lights[lights_index]
    else:
        s = "Incorrect value {} for instruction type".format(instruction_type)
        raise ValueError(s)


def update_lights(lights: Lights, instruction: Instruction):
    """
    Update all relevant lights according to Instruction
    """
    inst_type, x1, y1, x2, y2 = instruction

    # As we have flattened the 2-d grid by appending the rows to each other
    # col_num + GRID_WIDTH*row_num is the index of the light in lights
    for row_num in range(y1, y2+1):
        for col_num in range(x1, x2+1):
            update_light(lights, inst_type, col_num + GRID_WIDTH*row_num)


def main(filepath: str):
    instructions = parse_input(filepath)

    # array.array doesn't support higher dimensional arrays, so just use a
    # 1-d array. See docstring at top of page for more info.
    lights = array('h', (0 for _ in range(GRID_WIDTH**2)))

    for instruction in instructions:
        update_lights(lights, instruction)
    
    num_lights_on = sum(lights)

    print("There are {} lights on".format(num_lights_on))


if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'
    main(filepath)
