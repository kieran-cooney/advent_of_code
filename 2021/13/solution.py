import re
import numpy as np

DOT_PATTERN = re.compile(r"^(\d+),(\d+)$")
FOLD_PATTERN = re.compile(r"^fold along ([xy])=(\d+)$")


def parse_input(filepath):
    dots = list()
    folds = list()
    with open(filepath, 'r') as f:
        line = next(f)
        while not line.isspace():
            x, y = DOT_PATTERN.match(line).groups()
            dots.append((int(x), int(y)))
            line = next(f)
        
        for line in f:
            axis, n = FOLD_PATTERN.match(line).groups()
            folds.append((axis, int(n)))
    
    return dots, folds


def fold_1d(loc, fold):
    if loc <= fold:
        return loc
    else:
        return (2*fold) - loc


def fold_dot(dot, fold):
    x, y = dot
    axis, n = fold
    if axis == 'x':
        return (fold_1d(x, n), y)
    elif axis == 'y':
        return (x, fold_1d(y, n))


def fold_dots(dots, fold):
    return {fold_dot(d, fold) for d in dots}


def apply_all_folds(dots, folds):
    for fold in folds:
        dots = fold_dots(dots, fold)
    return dots


def get_dots_array(dots):
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)
    
    a = np.zeros((max_y+1, max_x+1), dtype=bool)

    for x, y in dots:
        a[y, x] = True
    
    return a


def print_dots_array(a):
    for line in a:
        s = ''.join('#' if e else '.' for e in line)
        print(s)
    return


def main(filepath):
    dots, folds = parse_input('input.txt')
    
    dots = fold_dots(dots, folds[0])
    print('{} points after 1 fold'.format(len(dots)))

    dots = apply_all_folds(dots, folds[1:])
    print_dots_array(get_dots_array(dots))


if __name__=='__main__':
    main('input.txt')