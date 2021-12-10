from functools import reduce

bracket_pairs = [
    ('()', 3, 1),
    ('{}', 1197, 3),
    ('<>', 25137, 4),
    ('[]', 57, 2)
]

close_to_open = {k: v for (v, k), *_ in bracket_pairs}
open_to_close = {k: v for (k, v), *_ in bracket_pairs}
corrupt_scores_dict = {k: v for (_, k), v, _ in bracket_pairs}
incomplete_scores_dict = {k: v for (_, k), _, v in bracket_pairs}
brackets, corrupt_scores, incomplete_scores = list(zip(*bracket_pairs))
opening_brackets, closing_brackets = list(zip(*brackets))


def parse_input(filepath):
    with open(filepath, 'r') as f:
        for l in f:
            yield l.strip()


def find_error(s):
    stack = list()
    for e in s:
        if e in opening_brackets:
            stack.append(e)
        elif e in closing_brackets:
            if not stack:
                return ('corrupt', e)
            elif close_to_open[e] != stack.pop():
                return ('corrupt', e)
    
    closing_chars = list()
    while stack:
        closing_chars.append(open_to_close[stack.pop()])
    
    closing_string = ''.join(closing_chars)

    return ('incomplete', closing_string)


def get_incomplete_score(s):
    char_scores = (incomplete_scores_dict[e] for e in s)
    return reduce(lambda x, y: (5*x)  + y, char_scores, 0)


def get_score(errors):
    corrupt_score = 0
    incomplete_scores = []
    for error_type, s in errors:
        if error_type == 'corrupt':
            corrupt_score += corrupt_scores_dict[s]
        elif error_type == 'incomplete':
            incomplete_scores.append(get_incomplete_score(s))
    
    incomplete_score = sorted(incomplete_scores)[len(incomplete_scores)//2]

    return corrupt_score, incomplete_score


def main(filepath):
    lines = parse_input(filepath)
    errors = (find_error(s) for s in lines)
    corrupt_score, incomplete_score = get_score(errors)
    print('Corrupt score: {}'.format(corrupt_score))
    print('Incomplete score: {}'.format(incomplete_score))

if __name__=='__main__':
    main('input.txt')