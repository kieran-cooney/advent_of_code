from solution import Board

test_board = Board("test_input.txt")

print(test_board.instructions)


for e in 'defghi':
    print(f"{e}: {test_board[e]}")