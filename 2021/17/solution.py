"""
Note that we assume that the target is always below and to the right of us.
"""

import re
import math

from collections import defaultdict
from itertools import count, takewhile, accumulate

INPUT_PATTERN = re.compile(
    r"^target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$"
)


def parse_input(filepath):
    with open(filepath, 'r') as f:
        line = next(f).strip()
    
    coords = INPUT_PATTERN.match(line).groups()
    
    return tuple(int(s) for s in coords)


def get_init_y_range(bottom_y, top_y):
    """
    Given the bottom and top y values of the target, return the lowest and
    highest v velocity values to check for.
    """
    # If the initial y velocity is v > 0, then the y coordinates will be
    # (v, 2v - 1, ..., v, 0, -v-1, ...)
    # So the values of [v-1, -v] will never be hit. We can use this to bound v
    return (bottom_y, -bottom_y-1)


def get_all_ys(init_y, bottom_y):
    """
    Given the initial y velocity and the bottom of the target, return a
    generator of all y values taken until the target is left
    """
    locs = accumulate(init_y - t for t in count())
    return takewhile(lambda y: y >= bottom_y, locs)


def get_all_xs(init_x):
    """
    Given the initial x velocity, return all x locations visted.
    """
    return accumulate(range(init_x, 0, -1))


def get_times_to_init_ys(bottom_y, top_y):
    """
    Given the bottom and top of the target, return a dictionary of the form {time: init_ys}, where locs is a list of all the initial y velocities which result in the y coordinate being in the target for time t.
    """
    data = defaultdict(list)
    min_init_y, max_init_y = get_init_y_range(bottom_y, top_y)

    for i in range(min_init_y, max_init_y + 1):
        results = get_all_ys(i, bottom_y)
        for t, y in enumerate(results, 1):
            if y in range(bottom_y, top_y+1):
                data[t].append(i)
    return data


def get_times_to_init_xs(left_x, right_x):
    """
    Given the left and right of the target, return a dictionary times and a
    list stucks.
    
    times is of the form {time: init_xs} where init_xs is a list of the init_x
    values for which there is a resulting x location in the target at time.
    stucks is a list of init_x for which the location ends up stuck with 
    velocity 0 in the target
    """
    times = defaultdict(list)
    stucks = list()

    for i in range(1, right_x + 1):
        for t, x in enumerate(get_all_xs(i), 1):
            if x in range(left_x, right_x+1):
                times[t].append(i)
    
        if x in range(left_x, right_x+1):
            stucks.append(i)
    
    return times, stucks


def get_all_initial_conditions(x_times, x_stucks, y_times):
    """
    Return a set {(init_x, init_y)} of pairs for which the initial conditions
    init_x, init_y result in a location in the target
    """
    sols = set()

    # Loop over times for which there was a value on target
    for t, init_ys in y_times.items():
        # Find the init_x values with location on target at the same time
        for init_x in x_times.get(t, []):
            for init_y in init_ys:
                sols.add((init_x, init_y))

        # Check if the y values descend through the target while x is 'stuck'
        for init_x in x_stucks:
            if t > init_x:
                for init_y in init_ys:
                    sols.add((init_x, init_y))
        
    return sols


def get_highest_height(sols):
    max_y = max(y for _, y in sols)
    return (max_y*(max_y + 1))//2


def main(filepath):
    # Get target coordinates
    x1, x2, y1, y2 = parse_input('input.txt')

    # Sort coordinates
    left_x, right_x = sorted([x1, x2])
    bottom_y, top_y = sorted([y1, y2])
    
    valid_y_sims = get_times_to_init_ys(bottom_y, top_y)
    valid_x_sims, stucks = get_times_to_init_xs(left_x, right_x)

    valid_initial_conditions = get_all_initial_conditions(valid_x_sims, stucks, valid_y_sims)
    
    print(len(valid_initial_conditions))
    print(get_highest_height(valid_initial_conditions))


if __name__=='__main__':
    main('input.txt')