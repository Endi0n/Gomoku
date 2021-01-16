import numpy as np
from strategies.heuristic import Heuristic
import re
from strategies.strategy import Strategy
from strategies.utils import contour, reverse_players


class Node:
    def __init__(self, alpha=None, beta=None):
        self.alpha = alpha
        self.beta = beta
        self.children = []
        self.parent = None

    def add_child(self, node):
        node.parent = self
        self.children.append(node)


class AbPruning(Strategy):
    def __init__(self, player, max_height=3):
        self.max_height = max_height
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

    def next_move(self, board):
        tree = Node()
        self._move(ab=True if self.player == 1 else False, node=tree, board=board)
        c, row, col = contour(board.board, 3)
        for i, node in enumerate(tree.children):
            if (node.beta == tree.alpha and self.player == 1) or (node.alpha == tree.beta and self.player == 2):
                board.place(np.argwhere(c == 0)[i] + [row, col], self.player)
                break

    def _score(self, board, player):
        if player == 1:
            return Heuristic.evaluate(board.board, patterns=self.patterns, cl=self.c)
        else:
            return -Heuristic.evaluate(reverse_players(board.board), patterns=self.patterns, cl=self.c)

    def _move(self, ab, node, board, height=0):
        c, i, j = contour(board.board, 3)

        for mv in np.argwhere(c == 0):
            n = Node()
            b = board.copy()
            b.place(mv + [i, j], 1 if ab else 2)
            node.add_child(n)
            if height + 2 == self.max_height:
                if ab is False:
                    n.alpha = self._score(b, 1)
                else:
                    n.beta = self._score(b, 2)
            else:
                self._move(not ab, node=n, height=height+1, board=b)

            if ab is False:
                # sunt pe beta
                if node.beta is None:
                    node.beta = n.alpha
                    continue

                if node.parent and node.parent.alpha is not None and node.beta <= node.parent.alpha:
                    break
                node.beta = min(node.beta, n.alpha)
            else:
                if node.alpha is None:
                    node.alpha = n.beta
                    continue

                if node.parent and node.parent.beta is not None and node.alpha >= node.parent.beta:
                    break
                node.alpha = max(node.alpha, n.beta)
