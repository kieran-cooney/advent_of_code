import sys
import numpy as np
from scipy.stats import mode


def parse_input(filepath):
    with open(filepath, 'r') as f:
        input_width = len(next(f).strip())

    print(input_width)

    col_widths = [1,]*input_width
    a = np.genfromtxt(
        filepath,
        delimiter=col_widths,
    )

    a = a.astype('bool')

    return a


def bin_array_to_dec(b_array):
    out = sum(2**i for i, b in enumerate(reversed(b_array)) if b)
    return out


def get_gen_rating(a, co2=False):
    out = a.copy()

    def filter(out, i):
        n = len(out)
        more_ones = (out[:, i].sum() >= n/2)
        x = 1 if (more_ones ^ co2) else 0
        sub_out = out[out[:, i] == x]
        return sub_out

    for i in range(out.shape[1]):
        if len(out) == 0:
            raise ValueError("Empty array at step {}".format(i))
        out = filter(out, i)
        if len(out) == 1:
            return bin_array_to_dec(out[0])

    raise ValueError("No rating found, {} rows left".format(len(out)))



def main(filepath):
    a = parse_input(filepath)

    gamma_bin = mode(a).mode[0]
    gamma = bin_array_to_dec(gamma_bin)
    width = len(gamma_bin)
    epsilon = (2**(width) - 1) - gamma

    print('Gamma rating: {}'.format(gamma))
    print('Epsilon rating: {}'.format(epsilon))
    print('Answer for part 1: {}'.format(epsilon*gamma))

    o2_rating = get_gen_rating(a)
    co2_rating = get_gen_rating(a, co2=True)
    print('O2 generator rating: {}'.format(o2_rating))
    print('C02 scrubber rating: {}'.format(co2_rating))
    print('Answer for part 2: {}'.format(o2_rating*co2_rating))


if __name__=='__main__':
    main(sys.argv[1])
