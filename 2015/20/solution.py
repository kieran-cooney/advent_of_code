"""
We make use of some mathematical bounds to skip on the smaller solutions.
We know that the sum of divisors is bounded above by some number, and so
we can skip all numbers for which we know the answer wil be less than what
we're looking for.

(Note that the number of presents at house n is related to the sum of divisors
of n.)

This solution assumes the Riemann hypothesis is true!

I think to speed this up further would require some parrelelism.
"""
from itertools import count

from math import ceil

import sympy as sp
from sympy.ntheory import divisor_sigma
from sympy import EulerGamma

TARGET = 33100000
SCALE_FACTOR = 10


def robins_upper_bound(n):
    """
    For all n > 5040, the sum of divisors of n is less than this
    https://en.wikipedia.org/wiki/Divisor_function
    """

    return sp.exp(EulerGamma) * n * sp.log(sp.log(n))


def robins_global_upper_bound(n):
    """
    Upper bound for the sum of divisors of n
    https://en.wikipedia.org/wiki/Divisor_function
    """
    return sp.Piecewise(
        (robins_upper_bound(n), n > 5040),
        (robins_upper_bound(n) + ((0.6483 * n)/(sp.log(sp.log(n)))), True)
    )


def get_lower_bound(target):
    """
    Given sum target, find the smallest possible n for which the
    sum of divisors could be as big as the target, according to
    robins upper bound
    """
    n = sp.Symbol('n')
    
    upper_bound = robins_global_upper_bound(n)
    guess = target*sp.exp(-EulerGamma).evalf()
    lower_bound = int(sp.nsolve(upper_bound - target, n, guess))
    
    return lower_bound


def get_first_house(target, start, verbose=True):
    """
    Given a target and starting value, find the first integer n greater than
    or equal to start such that the sum of divisors of n is at least as big as
    target
    """
    for i in count(start):
        num_presents = divisor_sigma(i)
        if num_presents >= target:
            return i
        if verbose and (i%1000) == 0:
            print('Calculating sum of divisors for {}'.format(i))


def main():
    target = ceil(TARGET/SCALE_FACTOR)
    print("Target presents after scaling down: {}".format(target))
    
    start = get_lower_bound(target)
    print("House number to start search from: {}".format(start))

    first_house = get_first_house(target, start)
    print(
        "First house number with {} presesnts: {}"
        .format(TARGET, first_house)
    )


if __name__=='__main__':
    main()
