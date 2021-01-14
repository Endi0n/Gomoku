import re
import numpy as np


def moves(board):
    return np.argwhere(board == 0)


def evaluate(board, patterns, c):
    score = 0
    for i, row in enumerate(board):
        s = ''.join(map(str, row))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))

    for i, row in enumerate(board.T):
        s = ''.join(map(str, row))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))

    for i in range(-board.shape[0] + 1, board.shape[0] - 1):
        s = ''.join(map(str, np.diag(board, i)))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))

    flipped_board = np.flip(board, 1)
    for i in range(-flipped_board.shape[0] + 1, flipped_board.shape[0] - 1):
        s = ''.join(map(str, np.diag(flipped_board, i)))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))
    return score


def next_move(board):
    patterns = {'11111': 100000,
                '011110': 9990,
                '01111': 9900,
                '01110': 50,
                '11100': 50,
                '01100': 40,
                '2221': 60,
                '2212': 60,
                '22122': 30000,
                '21222': 30000,
                '22221': 30000,
                '22222': -10000,
                '022220': -9999,
                '022200': -999,
                '02200': -300}
    c = re.compile(f"(?=({'|'.join(list(patterns.keys()) + [s[::-1] for s in patterns.keys()])}))")

    best = (None, None)
    for move in moves(board.board):
        board.place(move, 1)
        score = evaluate(board.board, patterns, c)
        if best[0] is None or score > best[0]:
            best = score, move
        board.remove(move)
    board.place(best[1], 1)
