import re

INPUT_PATTERN = re.compile(r"(\w+) (\d+)")

def parse_line(line):
    direction, num = re.match(INPUT_PATTERN, line).groups()
    num = int(num)
    return direction, num


def parse_input(filepath):
    with open(filepath, 'r') as f:
        output = [parse_line(l) for l in f]

    return output


def update_direction_pair_1(direction, num, loc):
    x, y = loc

    if direction == 'up':
        y -= num
    elif direction == 'down':
        y += num
    elif direction == 'forward':
        x += num

    return (x, y)


def update_direction_pair_2(direction, num, loc):
    x, y, aim = loc

    if direction == 'up':
        aim -= num
    elif direction == 'down':
        aim += num
    elif direction == 'forward':
        x += num
        y += aim*num
    else:
        raise ValueError("Bad direction {}".format(direction))

    return (x, y, aim)


def navigate_directions_list(dir_num_pairs, init_loc, update_func):
    loc = init_loc
    for direction, num in dir_num_pairs:
        loc = update_func(direction, num, loc)
    return loc


def get_answer(dir_num_pairs, init_loc, update_func, part_num):
    final_loc = navigate_directions_list(
        dir_num_pairs, init_loc, update_func
    )

    ans = final_loc[0]*final_loc[1]

    print('Location part {}: {}'.format(part_num, final_loc))
    print('Answer part {}: {}'.format(part_num, ans))



def main(filepath):
    dir_num_pairs = parse_input(filepath)

    get_answer(dir_num_pairs, (0, 0), update_direction_pair_1, 1)
    get_answer(dir_num_pairs, (0, 0, 0), update_direction_pair_2, 2)


if __name__=='__main__':
    main('input.txt')
