import re
import sys
from typing import NamedTuple, List, Tuple

class Reindeer(NamedTuple):
    name: str
    speed: int
    fly_duration: int
    rest_duration: int

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


def travel_distance(reindeer: Reindeer, duration: int) -> int:
    _, speed, fly_duration, rest_duration = reindeer

    period = fly_duration + rest_duration
    num_cycles, remainder = divmod(duration, period)

    remainder_fly_time = (
        fly_duration if fly_duration <= remainder else remainder
    )

    total_fly_time = remainder_fly_time + num_cycles*fly_duration
    total_distance = speed*total_fly_time

    return total_distance


def get_winning_reindeer(reindeers: List[Reindeer], duration: int) -> Tuple[str, int]:
    name_distance_pairs = (
        (r.name, travel_distance(r, duration))
        for r in reindeers
        )
    winning_reindeer = max(name_distance_pairs, key=lambda p: p[1])
    return winning_reindeer


def main(filepath: str, duration: int):
    reindeers = get_reindeers(filepath)
    winning_reindeer, distance = get_winning_reindeer(reindeers, duration)
    print(
        "{} is the winning reindeer, having travelled {} km in {} seconds!"
        .format(winning_reindeer, distance, duration)
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