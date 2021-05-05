"""
OOP solution using the following travelling salesman algorithm:
https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm
"""
import re
import sys
from collections import UserDict
from functools import lru_cache


class HappyPeople(UserDict):
    """
    Class containing the happiness gain of seating one poerson next to another
    as well as methods to compute the max gain in happiness.
    """
    # Used to parse input files.
    _INPUT_PATTERN = re.compile(r"^([A-Z][a-z]+) would (gain|lose) (\d+) happiness units by sitting next to ([A-Z][a-z]+)\.$")

    @staticmethod
    def tuple_sort(t):
        # Sort a tuple. Useful for ensuring unique keys in data
        return tuple(sorted(t))

    def __init__(self, *args):
        # self.data (comes with UserDict) contains happiness gains
        super().__init__(*args)
        # A set of all guests at the table
        self.guests = set()
        # A cache for calculating happiness later
        self.happiness_cache = dict()

    def __contains__(self, t):
        return self.tuple_sort(t) in self.data

    def __getitem__(self, t):
        # Wish to emulate defaultdict(int) behaviour here
        if t in self:
            return self.data[self.tuple_sort(t)]
        else:
            self.data[self.tuple_sort(t)] = 0
            return 0

    def __setitem__(self, t, value):
        # When adding a happiness gain, also add guest if necessary
        self.data[self.tuple_sort(t)] = value
        for g in t:
            self.guests.add(g)

    @classmethod
    def _parse_line(self, line):
        """
        Parse a single line of the input file
        """
        person1, sign, happiness, person2 = self._INPUT_PATTERN.match(line).groups()
        net_happiness = int(happiness) if sign == 'gain' else -1*int(happiness)
        return ((person1, person2), net_happiness)

    def parse_input(self, filepath):
        """
        Populate the  happiness dictionary from some file
        """
        with open(filepath, 'r') as f:
            for l in f.readlines():
                person_pair, happiness = self._parse_line(l)
                self[person_pair] += happiness

    def get_max_happiness_line(self, first, subset, last):
        """
        Get the max happiness if we arrange guests in a line, starting from
        first, ending in last, and seating everyone from subset in between

        Recursive solution

        Results are cached to self.happiness_cache
        """
        if not subset:
            return self[(first, last)]
        else:
            triple = (first, subset, last)
            if triple in self.happiness_cache:
                return self.happiness_cache[triple]
            else:
                ans = max(
                    self.get_max_happiness_line(first, subset - {other}, other) +
                    self[other, last]
                    for other in subset - {last}
                )
                self.happiness_cache[triple] = ans
                return ans

    def get_max_happiness_circle(self):
        """
        Get the max happiness possible if we seat all guests in some circle.
        """
        people = self.guests.copy()
        first_person = people.pop()
        people = frozenset(people)

        ans = max(
            self.get_max_happiness_line(first_person, people - {last}, last) +
            self[last, first_person]
            for last in people
        )

        return ans

def main(filepath):
    d = HappyPeople()
    d.parse_input(filepath)
    ans = d.get_max_happiness_circle()
    print(ans)

    old_party = d.guests.copy()
    for e in old_party:
        d[('Host', e)] = 0
    
    ans = d.get_max_happiness_circle()
    print(ans)

if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"
    main(filepath)