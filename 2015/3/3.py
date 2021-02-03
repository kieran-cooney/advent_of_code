from itertools import accumulate
from functools import reduce
from operator import add, or_
import sys

directions = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, 1),
    'v': (0, -1)
}


class Point:
    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
        elif len(args) == 1:
            pair = args[0]
            self.x = pair[0]
            self.y = pair[1]
        elif len(args) == 2:
            x, y = args
            self.x = x
            self.y = y
        else:
            raise TypeError("Point accepts 0, 1 or 2 argument constructors")

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, str):
            direction = directions.get(other, (0, 0))
            return self + Point(direction)
        else:
            raise TypeError("Only strings and Points can be added to point")

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return rf"({self.x}, {self.y})"


def read_directions(filepath: str ='input.txt') -> str:
    with open(filepath, 'r') as file:
        s = file.read()
    return s


def get_num_houses(directions_string: str, agents: int=1) -> int:
    agents_directions = [directions_string[i::agents] for i in range(agents)]

    agent_houses = (
        set(accumulate(directions, add, initial=Point()))
        for directions in agents_directions
    )

    visited_houses = reduce(or_, agent_houses)
    num_houses = len(visited_houses)

    return num_houses


def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'

    directions_string = read_directions(filepath)
    ans1, ans2 = [get_num_houses(directions_string, i) for i in [1, 2]]

    print(rf"Number of houses visited by Santa: {ans1}")
    print(rf"Number of houses visited by Santa and Robo Santa: {ans2}")


if __name__=='__main__':
    main()

