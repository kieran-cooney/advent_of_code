import sys
import numpy as np
from scipy.signal import convolve2d

NUM_ITERATIONS = 100

NEIGHBOURS = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])

def get_initial_lights(filepath):
    lights = np.zeros((100, 100))

    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.strip()):
                if c == '#':
                    lights[i, j] = 1
                elif c != '.':
                    raise ValueError("Invalid input character {} encountered.".format(c))

    return lights


def num_neigbours(lights):
    """
    Returns an array of the same shape as lights where each entry counts
    the number of neighbouring lights that are on in the array.

    1 1 0    3 3 2
    1 1 0 -> 3 3 2
    0 0 0    2 2 1
    """
    return convolve2d(lights, NEIGHBOURS, mode='same')


def update_lights(lights):
    num_neigbours_a = num_neigbours(lights)

    next_lights = (
        ((lights == 1) & ((num_neigbours_a == 2) | (num_neigbours_a == 3))) |
        ((lights == 0) & (num_neigbours_a == 3))
    )

    next_lights = next_lights.astype('int')

    return next_lights


def update_lights_repeatedly(lights, N=NUM_ITERATIONS):
    for _ in range(N):
        lights = update_lights(lights)
    return lights


def main(filepath):
    inital_lights = get_initial_lights(filepath)
    
    final_lights = update_lights_repeatedly(inital_lights)
    num_final_lights = np.sum(final_lights)

    print(
        'Number of lights on after {} iterations {}:'
        .format(NUM_ITERATIONS, num_final_lights)
    )


if __name__=='__main__': 
    if len(sys.argv) > 1: 
        filepath = sys.argv[1] 
    else: 
        filepath = "input.txt" 
    main(filepath) 