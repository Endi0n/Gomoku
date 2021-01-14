import re
import numpy as np


def moves(board):
    return np.argwhere(board == 0)


def evaluate(board, patterns, c):
    total_score = 0
    score = 0

    max_score = 0
    for i, row in enumerate(board):
        s = ''.join(map(str, row))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))
            max_score = max(score, max_score)
    total_score += max_score

    max_score = 0
    for i, row in enumerate(board.T):
        s = ''.join(map(str, row))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))
            max_score = max(score, max_score)
    total_score += max_score

    max_score = 0
    for i in range(-board.shape[0] + 1, board.shape[0] - 1):
        s = ''.join(map(str, np.diag(board, i)))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))
            max_score = max(score, max_score)
    total_score += max_score

    max_score = 0
    flipped_board = np.flip(board, 1)
    for i in range(-flipped_board.shape[0] + 1, flipped_board.shape[0] - 1):
        s = ''.join(map(str, np.diag(flipped_board, i)))
        for match in re.findall(c, s):
            score += patterns.get(match, patterns.get(match[::-1], 0))
            max_score = max(score, max_score)
    total_score += max_score

    return score


last_score = 0


def next_move(board):
    global last_score
    patterns = {'11111': 10 ** 2,
                '011110': 8 ** 2,
                '01111': 7 ** 2,
                '01110': 4 ** 2,
                '11100': 3 ** 2,
                '01100': 1 ** 2,
                '212': 1,
                '00111': 2 ** 2,
                '02221': 6 ** 2,
                '22210': 5 ** 2,
                '2212': 9 ** 2,
                '22122': 9 ** 2,
                '21222': 9 ** 2,
                '22221': 9 ** 2}
    c = re.compile(f"(?=({'|'.join(list(patterns.keys()) + [s[::-1] for s in patterns.keys()])}))")

    best = (None, None)
    for move in moves(board.board):
        board.place(move, 1)
        score = evaluate(board.board, patterns, c)
        print(score, last_score, move)
        score = score - last_score
        if best[0] is None or score > best[0]:
            best = score, move
        board.remove(move)
    print()
    last_score += best[0]
    board.place(best[1], 1)
