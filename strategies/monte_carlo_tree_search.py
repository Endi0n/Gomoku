import numpy as np
from strategies.heuristic import Heuristic
import random
from strategies.utils import contour
from strategies.strategy import Strategy


class Node:
    def __init__(self, player, board):
        self.w = 0
        self.n = 0
        self.score = 0
        self.board = board
        self.player = player
        self.children = []
        self.parent = None

    def add_child(self, node):
        node.parent = self
        self.children.append(node)


class MonteCarloTreeSearch(Strategy):
    def __init__(self):
        self.last_tree = None
        self.last_move_board = None

    def next_move(self, board, player):
        tree = None
        if self.last_tree:
            for child in self.last_tree.children:
                print(len(self.last_tree.children))
                if tree:
                    break
                if (child.board == self.last_move_board).all():
                    for ch in child.children:
                        if (ch.board == board).all():
                            tree = ch
                            print('HAHA')
                            break
        if tree is None:
            tree = Node(board=board, player=player)
        for _ in range(10):
            leaf, height = MonteCarloTreeSearch.selection(tree)
            new_node = MonteCarloTreeSearch.expansion(leaf, height)
            if new_node:
                result = MonteCarloTreeSearch.simulation(new_node)
                MonteCarloTreeSearch.backpropagation(new_node, result)

        m = 0
        for i, child in enumerate(tree.children[1:], 1):
            if child.n > tree.children[m].n:
                m = i
        # print(m)
        # print(tree.children[m].board.board)
        self.last_move_board = board.board[:, :] = tree.children[m].board.board
        self.last_tree = tree

    @staticmethod
    def selection(tree, height=0):
        if tree.children:
            chosen_node = (None, None)
            for child in tree.children:
                if child.w == 0 and child.n == 0:
                    return child, height

                winner = child.board.is_finished()
                if winner == 1:  # computer
                    child.score = np.inf
                    child.parent.score = -np.inf
                    return child
                else:
                    child.score = -np.inf

                if child.score != -np.inf:
                    child.score = child.w / child.n + np.sqrt(2 * np.log(tree.n)/child.n)

                if chosen_node[0] is None or child.score > chosen_node[0]:
                    chosen_node = child.score, child

            return MonteCarloTreeSearch.selection(chosen_node[1], height + 1)

        return tree, height

    @staticmethod
    def expansion(leaf, height):
        if leaf.score == np.inf:
            return None
        cont, row, col = contour(leaf.board.board, 3)
        m = np.argwhere(cont == 0)
        board = leaf.board.copy()
        random_moves = random.sample(list(m), len(m)//min(height + 1, 5))
        player = int(not (leaf.player - 1)) + 1
        for mv in random_moves:
            b = board.copy()
            b.place(mv + [row, col], leaf.player)
            node = Node(player, b)
            leaf.add_child(node)

        return random.choice(leaf.children)

    @staticmethod
    def simulation(tree):
        heuristic = Heuristic()
        board = tree.board.copy()
        player = tree.player
        x = 0
        p = random.randint(1, 3)
        while True:
            winner = board.is_finished()
            if winner:
                return winner
            if x == 4:
                if Heuristic.evaluate(board.board, heuristic.patterns, heuristic.c) < 0:
                    return 2
                else:
                    return 1
            if player == p:
                heuristic.next_move(board, player)
            else:
                m = np.argwhere(board.board == 0)
                board.place(m[np.random.randint(0, len(m))], player)
            player = int(not (player - 1)) + 1
            x += 1

    @staticmethod
    def backpropagation(leaf, result):
        node = leaf
        while True:
            if not node:
                break

            if result == node.player:
                node.w += 1
            node.n += 1

            node = node.parent


def play(board):
    player = 1
    print(board.board)
    s = MonteCarloTreeSearch()
    while True:
        winner = board.is_finished()
        # print('win:', winner)
        if winner:
            print('Winner:', winner)
            break
        if player == 1:
            s.next_move(board, 1)
        else:
            pos = list(map(int, input('Position: ').split()))
            board.place(pos, 2)
        player = int(not (player - 1)) + 1

        print(board.board)


from models.board import Board

if __name__ == '__main__':
    board = Board()
    play(board)
