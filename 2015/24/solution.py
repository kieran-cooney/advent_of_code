import sys
from functools import reduce
from itertools import combinations
from operator import mul


def parse_input(filepath):
    with open(filepath, 'r') as f:
        nums = sorted([int(l) for l in f])
    return nums


def get_qe(nums):
    # Compute the quantum entanglement of nums
    return reduce(mul, nums)


def get_target_weight(nums, n):
    sum_nums = sum(nums)
    if sum_nums % n != 0:
        raise ValueError("{} is not divisible by {}.".format(sum_nums, n))
    else:
        return sum_nums // n


def get_summing_nums(target, nums):
    if not nums:
        return []
    first, rest = nums[0], nums[1:]
    if first == target:
        yield [first]
    elif first < target:
        for l in get_summing_nums(target - first, rest):
            yield [first, *l]
        yield from get_summing_nums(target, rest)


def sort_summing_nums(summing_nums):
    sets = [set(l) for l in summing_nums]
    sets.sort(key = lambda l: (len(l), get_qe(l)))

    return sets


def optomise_packages(summing_sets, all_nums, num_compartments):
    if not summing_sets:
        return None
    first, rest = summing_sets[0], summing_sets[1:]
    
    print('Searching for solutions beginning with {}'.format(first))
    for i, combs in enumerate(combinations(rest, num_compartments - 1)):
        if i % 1000000 == 0:
            print('Searched {} combinations'.format(i))
        if first.union(*combs) == all_nums:
            return [first, *combs]
    
    return optomise_packages(rest, all_nums, num_compartments)


def solve(nums, num_compartments):
    target = get_target_weight(nums, 3)
    sum_combinations = sort_summing_nums(get_summing_nums(target, nums))

    print(sum_combinations[:5])
    print(sum_combinations[-5:])
    print(len(sum_combinations))

    set_nums = set(nums)

    return optomise_packages(sum_combinations, set_nums, num_compartments)

    
def main(filepath):
    nums = parse_input(filepath)
    sol = solve(nums, 3)
    min_qe = get_qe(sol[0])
    print(sol)
    print(min_qe)
    
if __name__=='__main__':
    if len(sys.argv) > 1:
          filepath = sys.argv[1]
    else:
          filepath = "input.txt"
    main(filepath)
