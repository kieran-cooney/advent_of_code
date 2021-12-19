import sys
import numpy as np


def parse_input(filepath):
    with open(filepath, 'r') as f:
        numbers = [int(x) for x in next(f).split(',')]

        cleaned_lines = (" ".join(l.strip().split()) for l in f)
        contents = [l for l in cleaned_lines if l != '']

        boards = (
            np.loadtxt(contents, dtype='int', delimiter=' ')
            .reshape(-1, 5, 5)
        )

    return numbers, boards


def check_for_bingo(marks):
    horizontals = np.all(marks, axis=1).any(axis=-1)
    if np.any(horizontals):
        return np.flatnonzero(horizontals)
    else:
        verticals = np.all(marks, axis=2).any(axis=-1)
        if np.any(verticals):
            return np.flatnonzero(verticals)

    return []


def get_score(board, marks, number):
    unmarked_sum = board[~marks].sum()
    return number*unmarked_sum
    

def play_bingo(numbers, boards):
    marks = np.zeros(boards.shape, dtype='bool')

    winners = list()

    for i, number in enumerate(numbers):
        new_marks = (boards == number)
        marks = new_marks | marks

        board_numbers = check_for_bingo(marks)
        new_board_numbers = [
            n for n in board_numbers
            if (n not in (b for b, *_ in winners))
        ]

        new_scores = [
            get_score(boards[n], marks[n], number)
            for n in new_board_numbers
        ]

        for b, s in zip(new_board_numbers, new_scores):
            winners.append((b, i, number, s))

    return winners


def main(filepath):
    numbers, boards = parse_input(filepath)

    print(len(numbers))
    print(boards.shape)
    winners = play_bingo(numbers, boards)
    print(len(winners))
    first_winner = winners[0]
    last_winner = winners[-1]
    print(last_winner)

    print("First winning board after {} numbers:".format(first_winner[1]))
    print(boards[first_winner[0]])
    print("Score: {}".format(first_winner[3]))

    print("Last winning board after {} numbers:".format(last_winner[1]))
    print(boards[last_winner[0]])
    print("Score: {}".format(last_winner[3]))

if __name__=='__main__':
    main(sys.argv[1])
