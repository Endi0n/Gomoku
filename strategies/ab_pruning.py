import numpy as np
import strategies.heuristic as heuristic
import re


class Node:
    def __init__(self, alpha=None, beta=None):
        self.alpha = alpha
        self.beta = beta
        self.children = []
        self.parent = None

    def add_child(self, node):
        node.parent = self
        self.children.append(node)


max_height = 3
N = 0


def next_move(board):
    global N
    tree = Node()
    N = 0
    move(ab=True, node=tree, board=board)
    for i, node in enumerate(tree.children):
        if node.beta == tree.alpha:
            board.place(np.argwhere(board.board == 0)[i], 1)
            break


patterns = {'11111': 120 ** 2,
            '011110': 9 ** 2,
            '0111010': 9 ** 2,
            '0110110': 10 ** 2,
            '01111': 8 ** 2,
            '10111': 8 ** 2,
            '01110': 4 ** 2,
            '11100': 2 ** 2,
            '01100': 2,
            '12': 1,
            '212': 2,
            '221': 3,
            '02221': 6 ** 2,
            '22210': 5 ** 2,
            '2212': 10 ** 2,
            '22122': 100 ** 2,
            '21222': 100 ** 2,
            '22221': 100 ** 2,
            # '02220': -7 ** 2,

            '22222': -120 ** 2,
            '022220': -9 ** 2,
            '0222020': -9 ** 2,
            '0220220': -10 ** 2,
            '02222': -8 ** 2,
            '20222': -8 ** 2,
            '02220': -4 ** 2,
            '22200': -2 ** 2,
            '02200': -2,
            '21': -1,
            '121': -2,
            '112': -3,
            '01112': -6 ** 2,
            '11120': -5 ** 2,
            '1121': -10 ** 2,
            '11211': -100 ** 2,
            '12111': -100 ** 2,
            '11112': -100 ** 2
            # '01110': 7 ** 2
            }
c = list(map(re.compile, list(patterns.keys()) + ([s[::-1] for s in patterns.keys()])))
c.sort(key=lambda k: len(k.pattern), reverse=True)


def score(board):
    return heuristic.evaluate(board.board, patterns=patterns, cl=c)


def move(ab, node, board, height=0):
    global max_height, N
    print(N)
    for mv in np.argwhere(board.board == 0):
        N += 1
        n = Node()
        b = board.copy()
        b.place(mv, 1 if ab else 2)
        node.add_child(n)
        if height + 2 == max_height:
            if ab is False:
                n.alpha = score(b)
            else:
                n.beta = score(b)
        else:
            move(not ab, node=n, height=height+1, board=b)

        if ab is False:
            # sunt pe beta
            if node.beta is None:
                node.beta = n.alpha
                continue

            if node.parent.alpha is not None and node.beta <= node.parent.alpha:
                break
            node.beta = min(node.beta, n.alpha)
        else:
            if node.alpha is None:
                node.alpha = n.beta
                continue

            if node.parent and node.parent.beta is not None and node.alpha >= node.parent.beta:
                break
            node.alpha = max(node.alpha, n.beta)
