"""
An overkill solution.

The overall strategy comes from observing that we need to calculate

INITIAL * (SCALER ^ power) (mod QUOTIENT)

so we can do some nice maths to simplify some things.

1) Since the quotient is prime, we can use Fermat's little theorem to simplify
the expression.
2) Observe that if p = 2^n, then x^p = x^(2^n), which is the same as squaring
x repeatedly n times. This is exponentially faster than multiplying x by
itself 2^n times! Then if we write power as a binary number, this is a sum of
powers of 2, and so we can calculate (SCALER ^ power) exponentially fast using
this trick.

NOTE: We use the concept of 'modular arithmetic' frequently. This just means
finding the remainder of all results upon division by QUOTIENT.
"""
import sys
from functools import reduce
import re

INPUT_PATTERN = re.compile(r"To continue, please consult the code grid in the manual.  Enter the code at row (\d*), column (\d*).")

QUOTIENT = 33554393
SCALER = 252533
INITIAL = 20151125


def parse_input(filepath):
    with open(filepath, 'r') as file:
        string = file.read()
        y, x = INPUT_PATTERN.match(string).groups()
        x = int(x)
        y = int(y)
    return x, y


def coords_to_index(x, y):
    top_row_diag_intersection = (x + y - 1)*(x + y)//2
    offset = -y
    return top_row_diag_intersection + offset


def reduce_index(i):
    """
    Assuming the quotient is prime (which in this case, it is), can apply
    FLT
    https://en.wikipedia.org/wiki/Fermat's_little_theorem
    
    But to be fully general, should check QUOTIENT is prime using sympy
    """
    return i % (QUOTIENT - 1)


def modulo_mul(x, y, quotient=QUOTIENT):
    """
    Multiply x by y modulo quotient.
    """
    return (x*y) % quotient


def modulo_square(x, quotient=QUOTIENT):
    """
    Calculate x squared modulo quotient
    """
    return modulo_mul(x, x, quotient)


def modulo_power(power, base=SCALER, quotient=QUOTIENT):
    """
    Calculate base^power (mod quotient)
    """
    # Get the binary representation of power, remove first two characters
    # and reverse
    bin_power = bin(power)[:1:-1]

    # List of [base, base^2, base^(2^2), base^(2^3), ...]
    squares = [base]
    for _ in bin_power[1:]:
        squares.append(modulo_square(squares[-1]))

    # Get the factors to multiply together. Will only multiply a square of
    # there is a '1' in the corresponding position in the binary representation
    factors = [s for i, s in zip(bin_power, squares) if i =='1']

    return reduce(modulo_mul, factors, 1)


def main(filepath):
    x, y = parse_input(filepath)
    index = coords_to_index(x, y)

    overall_factor = modulo_power(index)
    ans = modulo_mul(INITIAL, overall_factor)

    print(ans)


if __name__=='__main__':
    if len(sys.argv) > 1:
          filepath = sys.argv[1]
    else:
          filepath = "input.txt"
    main(filepath)
