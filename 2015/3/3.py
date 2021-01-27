from itertools import accumulate
from operator import add

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


def get_num_houses(directions_string: str) -> int:
    return len(set(accumulate(directions_string, add, initial=Point())))


def main():
    num_houses = get_num_houses(read_directions())
    print(rf"Number of houses visited: {num_houses}")


if __name__=='__main__':
    main()
