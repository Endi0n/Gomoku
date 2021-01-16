import numpy as np


def contour(board, k):
    pos = np.argwhere(board != 0).T
    if pos.shape[1] == 0:
        pos = [[0, board.shape[0]], [0, board.shape[1]]]
    i, j = max(min(pos[0])-k, 0), max(min(pos[1])-k, 0)
    return board[i:min(max(pos[0])+k, board.shape[0])+1,
                 j:min(max(pos[1])+k, board.shape[1])+1], i, j


def reverse_players(board, players=(1, 2)):
    board_copy = board.copy()
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == players[0]:
                board_copy[i][j] = players[1]
            elif board[i][j] == players[1]:
                board_copy[i][j] = players[0]
    return board_copy
