import sys
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def parse_input(filename):
    a = np.loadtxt(filename, dtype='int')

    return a

def get_ans1(nums):
    depth_increase = (nums[1:] > nums[:-1])
    return sum(depth_increase)

def get_ans2(nums, window_length=3):
    rolling_sums = np.sum(sliding_window_view(nums, window_length), axis=1)
    
    depth_increase = (rolling_sums[1:] > rolling_sums[:-1])

    return sum(depth_increase)


if __name__=='__main__':
    cl_args = sys.argv
    if len(cl_args) > 1:
        input_file = cl_args[1]
    else:
        input_file = 'input.txt'

    nums = parse_input(input_file)

    ans1 = get_ans1(nums)
    print(ans1)

    ans2 = get_ans2(nums)
    print(ans2)