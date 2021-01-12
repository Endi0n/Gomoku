import numpy as np


class Board:
    EMPTY_CELL = 0
    PIECE_A = 1
    PIECE_B = 2

    def __init__(self, size=19):
        self.board = np.zeros((size, size), dtype=np.uint8)

    def place(self, location, piece):
        pass

    @staticmethod
    def _check_row(row):
        if len(row) < 5:
            return None

        last_p = row[0]
        count_p = 1

        for p in row[1:]:
            if p != Board.EMPTY_CELL:
                continue

            if p == last_p:
                count_p += 1
                if count_p == 5:
                    return last_p
            else:
                last_p = p
                count_p = 1

        return None

    def is_finished(self):
        def check_rows(rows):
            for row in rows:
                winner = Board._check_row(row)

                if winner:
                    return winner

        return check_rows(self.board) or check_rows(self.board.T) or None
