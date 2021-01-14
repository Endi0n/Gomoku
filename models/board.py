import numpy as np


class Board:
    EMPTY_CELL = 0
    PIECE_A = 1
    PIECE_B = 2

    def __init__(self, size=19):
        self.size = size
        self.board = np.zeros((size, size), dtype=np.uint8)

    def place(self, location, piece):
        self.board[tuple(location)] = piece

    def remove(self, location):
        self.board[tuple(location)] = Board.EMPTY_CELL

    @staticmethod
    def _check_row(row):
        if len(row) < 5:
            return None

        last_p = row[0]
        count_p = 1

        for p in row[1:]:
            if p == Board.EMPTY_CELL:
                continue

            if p == last_p:
                count_p += 1
                if count_p == 5:
                    return last_p
            else:
                last_p = p
                count_p = 1

        return None

    @staticmethod
    def diagonals(board):
        diagonals = []
        for i in range(-board.shape[0]+1, board.shape[0]-1):
            diagonals.append(np.diag(board, i))
        return diagonals

    def is_finished(self):
        def check_rows(rows):
            for row in rows:
                winner = Board._check_row(row)

                if winner:
                    return winner

        return check_rows(self.board) or check_rows(self.board.T) or\
            check_rows(Board.diagonals(self.board)) or check_rows(Board.diagonals(np.flip(self.board, 1))) or None

    def copy(self):
        board = Board(self.size)
        board.board[:, :] = self.board
        return board
