import re
import sys
from typing import NamedTuple, List, Tuple, Iterator
from itertools import repeat, chain, cycle, accumulate
from collections import defaultdict
from operator import itemgetter

class Reindeer(NamedTuple):
    name: str
    speed: int
    fly_duration: int
    rest_duration: int

class WinningReindeer(NamedTuple):
    name: str
    score: int

INPUT_FILEPATH = 'input.txt'
DURATION = 2503
REINDEER_PATTERN = re.compile(
    r"^([A-Z][a-z]+) can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds.$"
)


def parse_line(line: str) -> Reindeer:
    regex_groups = REINDEER_PATTERN.match(line).groups()

    name, *numbers = regex_groups
    numbers = [int(i) for i in numbers]

    reindeer = Reindeer(name, *numbers)

    return reindeer


def get_reindeers(filepath: str) -> List[Reindeer]:
    reindeers = list()
    with open(filepath, 'r') as f:
        for line in f:
            reindeers.append(parse_line(line))
    
    return reindeers


def distance_iterator(reindeer: Reindeer) -> Iterator[int]:
    """
    Return an (infinite) iterator of how far the reindeer has travelled at
    every second
    """
    _, speed, fly_duration, rest_duration = reindeer

    fly_increments = repeat(speed, fly_duration)
    rest_increments = repeat(0, rest_duration)

    cycle_increments = chain(fly_increments, rest_increments)
    increments = cycle(cycle_increments)

    distances = accumulate(increments)

    return distances


def score_reindeers(reindeers: List[Reindeer], duration: int) -> Tuple[WinningReindeer, WinningReindeer]:
    """
    Get the winning reindeers for both parts with their respective score
    """
    scores = defaultdict(int)

    iterators = [(r.name, distance_iterator(r)) for r in reindeers]

    for _ in range(duration):
        winner, distance = max(
            ((name, next(it)) for name, it in iterators),
            key=itemgetter(1)
        )
        
        scores[winner] += 1
    
    winner_1 = WinningReindeer(winner, distance)
    winner_2 = max(
        ((name, score)for name, score in scores.items()),
        key=itemgetter(1)
    )
    winner_2 = WinningReindeer(*winner_2)

    return winner_1, winner_2


def main(filepath: str, duration: int):
    reindeers = get_reindeers(filepath)
    winner_1, winner_2 = score_reindeers(reindeers, duration)
    print(
        "{} is the winning reindeer for part 1, having travelled {} km in {} seconds!"
        .format(winner_1.name, winner_1.score, duration)
    )
    print(
        "{} is the winning reindeer for part 2, having scored {} points in {} seconds!"
        .format(winner_2.name, winner_2.score, duration)
    )


if __name__=='__main__':
    num_args = len(sys.argv) - 1
    if num_args > 2:
        raise ValueError("No more than two arguments excepted")
    elif num_args == 2:
        main(sys.argv[1], int(sys.argv[2]))
    elif num_args == 1:
        main(sys.argv[1], DURATION)
    else:
        main(INPUT_FILEPATH, DURATION)