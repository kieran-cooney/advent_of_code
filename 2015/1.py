from itertools import accumulate

with open(r"inputs/1.txt") as file:
    brackets = file.read()

def char_value(c):
    if c == '(':
        return 1
    elif c == ')':
        return -1
    else:
        return 0

bracket_values = [char_value(c) for c in brackets]
floor_nums = list(accumulate(bracket_values))

last_floor_num = floor_nums[-1]
print(rf'Answer for part 1: {last_floor_num}')

negative_floor_positions = (
    i for i, n in enumerate(floor_nums, start=1) if n < 0
)

first_negative_floor_position = next(negative_floor_positions)
print(rf'Answer for part 1: {first_negative_floor_position}')
