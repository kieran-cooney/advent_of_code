import re
import numpy as np

LINE_PATTERN = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


def sym_arange(start, stop):
    if stop > start:
        return np.arange(start, stop + 1)
    else:
        return np.arange(start, stop-1, step=-1)


def parse_input(filepath):
    with open(filepath, 'r') as f:
        lines = (LINE_PATTERN.match(l).groups() for l in f)

        a = (
            np.fromiter(lines, dtype='int,int,int,int')
            .view('int')
            .reshape(-1, 2, 2)
        )

    return a


def get_seafloor_grid(vents_array):
    max_x, max_y = vents_array.max(axis=(0, 1))
    return np.zeros((max_x+1, max_y+1), dtype='int')


def count_vents(vents_array):
    va = vents_array

    counts_array = get_seafloor_grid(va)

    is_horizontal = (va[:, 0, 1] == va[:, 1, 1])
    horizontal_vents = va[is_horizontal]

    is_vertical = (va[:, 0, 0] == va[:, 1, 0])
    vertical_vents = va[is_vertical]

    is_up_diag = (va[:, 1, 0] - va[:, 0, 0]) == (va[:, 1, 1] - va[:, 0, 1])
    up_diag_vents = va[is_up_diag]

    is_down_diag = (va[:, 1, 0] - va[:, 0, 0]) == -(va[:, 1, 1] - va[:, 0, 1])
    down_diag_vents = va[is_down_diag]

    for (x1, y), (x2, _) in horizontal_vents:
        x1, x2 = sorted([x1, x2])
        counts_array[x1:(x2+1), y] += 1

    for (x, y1), (_, y2) in vertical_vents:
        y1, y2 = sorted([y1, y2])
        counts_array[x, y1:(y2+1)] += 1

    ans1 = (counts_array >= 2).sum()

    for (x1, y1), (x2, y2) in up_diag_vents:
        x_indices = sym_arange(x1, x2)
        y_indices = sym_arange(y1, y2)
        counts_array[x_indices, y_indices] += 1

    for (x1, y1), (x2, y2) in down_diag_vents:
        x_indices = sym_arange(x1, x2)
        y_indices = sym_arange(y1, y2)
        counts_array[x_indices, y_indices] += 1

    ans2 = (counts_array >= 2).sum()

    print(ans1)
    print(ans2)

a = parse_input('input.txt')
count_vents(a)
