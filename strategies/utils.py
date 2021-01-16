import numpy as np


def contour(board, k):
    pos = np.argwhere(board != 0).T
    if pos.shape[1] == 0:
        pos = [[0, board.shape[0]], [0, board.shape[1]]]
    i, j = max(min(pos[0])-k, 0), max(min(pos[1])-k, 0)
    return board[i:min(max(pos[0])+k, board.shape[0])+1,
                 j:min(max(pos[1])+k, board.shape[1])+1], i, j
