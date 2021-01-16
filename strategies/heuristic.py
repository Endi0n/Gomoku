import re
import numpy as np
import random
from strategies.utils import contour, reverse_players
from strategies.strategy import Strategy


class Heuristic(Strategy):
    def __init__(self, player):
        self.last_score = 0
        self.player = player
        self.patterns = {'11111': 120 ** 2,
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
        self.c = list(map(re.compile, list(self.patterns.keys()) + ([s[::-1] for s in self.patterns.keys()])))
        self.c.sort(key=lambda k: len(k.pattern), reverse=True)

    @staticmethod
    def evaluate(board, patterns, cl):
        board, i, j = contour(board, 1)

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

    def next_move(self, board):
        board_copy = board.copy()
        options = []
        for move in np.argwhere(board.board == 0):
            board_copy.place(move, self.player)
            if self.player == 1:
                score = Heuristic.evaluate(board_copy.board, self.patterns, self.c)
            else:
                score = Heuristic.evaluate(reverse_players(board_copy.board), self.patterns, self.c)
            # print(score, last_score, move)
            score = score - self.last_score
            options.append((score, move))
            board_copy.remove(move)
        # print()

        options.sort(key=lambda k: k[0], reverse=True)
        options = [option for option in options if option[0] == options[0][0]]

        choice = random.choice(options)
        self.last_score += choice[0]
        board.place(choice[1], self.player)
