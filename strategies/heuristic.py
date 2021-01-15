import re
import numpy as np
import random


def moves(board):
    return np.argwhere(board == 0)


def evaluate(board, patterns, cl):
    def sub_evaluate(line):
        score = 0
        for c in cl:
            for match in re.findall(c, line):
                score += patterns.get(match, patterns.get(match[::-1], 0))
        return score

    score = 0

    for i, row in enumerate(board):
        score += sub_evaluate(''.join(map(str, row)))

    for i, row in enumerate(board.T):
        score += sub_evaluate(''.join(map(str, row)))

    for i in range(-board.shape[0] + 1, board.shape[0] - 1):
        score += sub_evaluate(''.join(map(str, np.diag(board, i))))

    flipped_board = np.flip(board, 1)
    for i in range(-flipped_board.shape[0] + 1, flipped_board.shape[0] - 1):
        score += sub_evaluate(''.join(map(str, np.diag(flipped_board, i))))

    return score


last_score = 0
patterns = {'11111': 120 ** 2,
            '011110': 9 ** 2,
            '0111010': 9 ** 2,
            '0110110': 10 ** 2,
            '01111': 8 ** 2,
            '10111': 8 ** 2,
            '010110': 4.5 ** 2,
            '10110': 4.5 ** 2,
            '01110': 4 ** 2,
            '11100': 2 ** 2,
            '01100': 2,
            '01010': 2,
            '12': 1,
            '212': 2,
            '221': 3,
            '02221': 6 ** 2,
            '22210': 5 ** 2,
            '2212': 10 ** 2,
            '22122': 100 ** 2,
            '21222': 100 ** 2,
            '22221': 100 ** 2,
            '02220': -7 ** 2,
            '2020': -7 ** 2,
            '020220': -8 ** 2,
            }
c = list(map(re.compile, list(patterns.keys()) + ([s[::-1] for s in patterns.keys()])))
c.sort(key=lambda k: len(k.pattern), reverse=True)


def next_move(board):
    board_original = board
    board = board.copy()

    global last_score, c, patterns

    options = []
    for move in moves(board.board):
        board.place(move, 1)
        score = evaluate(board.board, patterns, c)
        # print(score, last_score, move)
        score = score - last_score
        options.append((score, move))
        board.remove(move)
    # print()

    options.sort(key=lambda k: k[0], reverse=True)
    options = [option for option in options if option[0] == options[0][0]]

    choice = random.choice(options)
    last_score += choice[0]
    board_original.place(choice[1], 1)
