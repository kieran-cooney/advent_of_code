import re
import sys
from operator import itemgetter
from itertools import permutations
from typing import Tuple, Dict, List, Iterable, Callable

Locations = List[str]
LocationPair = Tuple[str, str]
DistanceDict = Dict[LocationPair, int]
Path = List[str]

DISTANCE_PATTERN = re.compile(r"^(\w+)\sto\s(\w+)\s=\s(\d+)$")

def parse_line(line: str) -> Tuple[str, str, int]:
    l1, l2, distance = DISTANCE_PATTERN.match(line.strip()).groups()
    distance = int(distance)

    return l1, l2, distance


def load_file(filepath: str) -> Tuple[DistanceDict, Locations]:
    d = dict()
    locations = set()

    with open(filepath) as f:
        for line in f:
            l1, l2, dist = parse_line(line)
            pair = tuple(sorted([l1, l2]))
            d[pair] = dist

            locations.add(l1)
            locations.add(l2)

    locations = sorted(locations)

    return d, locations


def path_distance(path: Path, d: DistanceDict) -> int:
    loc_pairs = (
        tuple(sorted(pair))
        for pair in zip(path[:-1], path[1:])
    )

    distance = sum(d[pair] for pair in loc_pairs)

    return distance


def extremal_path_pair(d: DistanceDict, l: Locations,
    key: Callable=itemgetter(1)) -> Tuple[Path, int]:
    paths = permutations(l)
    paths_with_distances = ((path, path_distance(path, d)) for path in paths)
    shortest_path_pair = min(paths_with_distances, key=key)

    return shortest_path_pair


def main(filepath):
    d, l = load_file(filepath)
    shortest_path, shortest_distance = extremal_path_pair(d, l)
    longest_path, longest_distance = extremal_path_pair(
        d, l, lambda p: -1*itemgetter(1)(p)
    )

    print("Answer for part 1: {}".format(shortest_distance))
    print("Path for part 1: {}".format(shortest_path))


    print("Answer for part 1: {}".format(longest_distance))
    print("Path for part 1: {}".format(longest_path))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'
    main(filepath)
