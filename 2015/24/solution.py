import sys
from functools import reduce
from itertools import chain
from operator import mul


def parse_input(filepath):
    with open(filepath, 'r') as f:
        nums = [int(l) for l in f]
    return nums


def get_target_weight(nums, n):
    sum_nums = sum(nums)
    if sum_nums % n != 0:
        raise ValueError("{} is not divisible by {}.".format(sum_nums, n))
    else:
        return sum_nums // n


def all_k_true_n_sequences(n, k):
    """
    Returns a generator producing all boolean lists of length n
    with k true values
    """
    if k == 0:
        yield [False, ] * n
    elif k > n:
        pass
    else:
        for s in all_k_true_n_sequences(n-1, k-1):
            yield [True, *s]
        for s in all_k_true_n_sequences(n-1, k):
            yield [False, *s]


def all_bool_n_sequences(n):
    """
    Returns a generator producing all boolean lists of length n
    """
    if n == 0:
        yield []
    else:
        for s in all_bool_n_sequences(n-1):
            yield [True, *s]
            yield [False, *s]


def bool_index(seq, bool_seq, neg=False):
    """
    Numpy boolean indexing but for python lists
    """
    if not neg:
        return [s for s, b in zip(seq, bool_seq) if b]
    else:
        return [s for s, b in zip(seq, bool_seq) if not b]


def split_k_from_seq(seq, k):
    """
    Return all possible pairs (k_seq, rest) where k_seq is some subsequence
    of k elemenets from seq, and rest is the rest.
    
    Like itertools.combinations, but with rest
    """
    n = len(seq)
    for bool_seq in all_k_true_n_sequences(len(seq), k):
        yield (bool_index(seq, bool_seq), bool_index(seq, bool_seq, True))


def split_seq_in_2(seq):
    """
    Return all possible pairs (seq1, seq2) where seq1 and seq2 are
    subsequences of seq whose union is seq
    """
    if not seq:
        pass
    else:
        first, *rest = seq
        for bool_seq in all_bool_n_sequences(len(rest)):
            seq1 = [first, *bool_index(rest, bool_seq)]
            seq2 = bool_index(rest, bool_seq, True)
            yield (seq1, seq2)

            
def split_seq_in_n(seq, n):
    """
    Return all possible n-lists [seq1, seq2, ..., seqn] where seqi is a sub
    sequence of seq and the union of all subsequences is seq
    """
    if n  == 1:
        yield [seq]
    else:
        for seq1, seq2 in split_seq_in_2(seq):
            for seqs in split_seq_in_n(seq2, n-1):
                yield [seq1, *seqs]


def get_qe(nums):
    # Compute the quantum entanglement of nums
    return reduce(mul, nums)


def split_packages_in_n(nums, target_weight, n):
    """
    Return all possible n-lists of subsequences of nums where
    each subsequence sums to target_weight
    """
    for seqs in split_seq_in_n(nums, n):
        if all(sum(s) == target_weight for s in seqs):
            yield seqs


def find_sols_fixed_k(k, nums, target_weight, n):
    """
    Find all the solutions to santas problem assuming there are k packages
    in santa's passenger compartment
    
    Further, sort the solutions by quantum entanglement
    """
    possible_sols = (
        (first_nums, rest, get_qe(first_nums))
        for first_nums, rest in split_k_from_seq(nums, k)
        if sum(first_nums) == target_weight
    )

    possible_sols = sorted(possible_sols, key=lambda t: t[-1])

    for first, rest, qe in possible_sols:
        for seq in split_packages_in_n(rest, target_weight, n-1):
            yield (first, *seq, qe)


def get_all_sols(nums, n, verbose=True):
    """
    Return a generator of all solutions to the problem
    
    Iterate over the number of packages in the passenger compartment,
    so that the first solution we find is optimal.
    """
    target_weight = get_target_weight(nums, n)

    for k in range(1, len(nums)):
        if verbose:
            print('Searching solutions with {} presents in passenger compartment'.format(k))
        for s in find_sols_fixed_k(k, nums, target_weight, n):
            yield s


def find_sols(nums, n):
    """
    Get a generator of all solutions, and then get the first solution to find
    the optimal
    """
    all_sols = get_all_sols(nums, n)

    return next(all_sols)


def main(filepath):
    nums = parse_input(filepath)
    
    print("\nThree groups of presents:")
    sol1 = find_sols(nums, 3)
    print(sol1)

    # Part 2... but won't work!
    """
    print("\nFour groups of presents:")
    sol2 = find_sols(nums, 4)
    print(sol2)
    """

if __name__=='__main__':
    if len(sys.argv) > 1:
          filepath = sys.argv[1]
    else:
          filepath = "input.txt"
    main(filepath)
