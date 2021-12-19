from collections import Counter

def parse_input(filepath):
    with open(filepath, 'r') as f:
        line = next(f)
    nums = [int(x) for x in line.split(',')]
    num_counts = Counter(nums)
    
    out = [0]*9
    
    for k, v in num_counts.items():
        out[k] = v

    return out

def step_fish_day(day_counts):
    new_fish = day_counts[0]
    day_counts[:-1] = day_counts[1:]
    day_counts[-1] = new_fish
    day_counts[6] += new_fish
    pass


def lanternfish_model(initial_day_counts, num_days):
    day_counts = initial_day_counts.copy()
    for _ in range(num_days):
        step_fish_day(day_counts)
    return day_counts


def main(filepath):
    day_counts = parse_input(filepath)
    result1 = lanternfish_model(day_counts, 80)
    result2 = lanternfish_model(result1, 256-80)
    print("Answers: {} & {}".format(sum(result1), sum(result2)))


if __name__=='__main__':
    main('input.txt')