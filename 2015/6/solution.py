"""
Solution to day 6 of advent of code 2015: https://adventofcode.com/2015/day/6

Friendship ended with array.array
numpy.array is my new best friend
"""

import re
import sys

import numpy as np
from typing import Tuple, Iterable

Instruction = Tuple[str, int, int, int, int]
Lights = Iterable

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


def update_lights1(lights: Lights, instruction: Instruction):
    """
    Update all relevant lights according to Instruction
    """
    inst_type, x1, y1, x2, y2 = instruction

    sub_lights = lights[x1:x2+1,y1:y2+1]

    if inst_type == "turn on":
        sub_lights[:] = True
    elif inst_type == "turn off":
        sub_lights[:] = False
    elif inst_type == "toggle":
        np.invert(sub_lights, sub_lights) 
    else:
        raise ValueError("Invalid instruction type: " + inst_type)


def update_lights2(lights: Lights, instruction: Instruction):
    """
    Update all relevant lights according to Instruction for part 2
    """
    inst_type, x1, y1, x2, y2 = instruction

    sub_lights = lights[x1:x2+1,y1:y2+1]

    if inst_type == "turn on":
        sub_lights += 1
    elif inst_type == "turn off":
        sub_lights[sub_lights > 0] -= 1
    elif inst_type == "toggle":
        sub_lights += 2
    else:
        raise ValueError("Invalid instruction type: " + inst_type)


def update_lights(lights: Lights, instruction: Instruction, part: int):
    if part == 1:
        return update_lights1(lights, instruction)
    elif part == 2:
        return update_lights2(lights, instruction)
    else:
        raise ValueError("Invalid part number: {}".format(part))


def main(filepath: str, part: int):
    instructions = parse_input(filepath)

    if part == 1:
        lights = np.zeros((GRID_WIDTH, GRID_WIDTH), dtype=bool)
    if part == 2:
        lights = np.zeros((GRID_WIDTH, GRID_WIDTH))

    for instruction in instructions:
        update_lights(lights, instruction, part)
    
    num_lights_on = int(np.sum(lights))

    print("There are {} lights on".format(num_lights_on))


if __name__=='__main__':
    if len(sys.argv) > 3:
        print('Invalid number of arguments provided. Only two required, filepath and part number.')
    if len(sys.argv) == 3:
        filepath = sys.argv[1]
        part = int(sys.argv[2])
    elif len(sys.argv) == 2:
        filepath = sys.argv[1]
        part = 2
    else:
        filepath = 'input.txt'
        part=2
    main(filepath, part)
