import numpy as np


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


def moves(board):
    return np.argwhere(board == 0)


def selection(tree):
    if tree.children:
        chosen_node = (None, None)
        for child in tree.children:
            if child.w == 0 and child.n == 0:
                return child

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

        return selection(chosen_node[1])

    return tree


def expansion(leaf):
    if leaf.score == np.inf:
        return None
    m = moves(leaf.board.board)
    board = leaf.board.copy()
    board.place(m[np.random.randint(0, len(m))], leaf.player)
    player = int(not (leaf.player - 1)) + 1
    node = Node(player, board)
    leaf.add_child(node)
    return node


def simulation(tree):
    board = tree.board.copy()
    player = tree.player
    while True:
        winner = board.is_finished()
        if winner:
            return winner
        m = moves(board.board)
        board.place(m[np.random.randint(0, len(m))], player)
        player = int(not (player - 1)) + 1


def backpropagation(leaf, result):
    node = leaf
    while True:
        if not node:
            break

        if result == node.player:
            node.w += 1
        node.n += 1

        node = node.parent


def next_move(board):
    tree = Node(board=board, player=1)

    for _ in range(30):
        leaf = selection(tree)
        new_node = expansion(leaf)
        if new_node:
            result = simulation(new_node)
            backpropagation(new_node, result)

    m = 0
    for i, child in enumerate(tree.children[1:], 1):
        if child.n > tree.children[m]:
            m = i
    board.board[:, :] = tree.children[m].board.board


def play(board):
    player = 1
    print(board.board)
    while True:
        winner = board.is_finished()
        # print('win:', winner)
        if winner:
            print('Winner:', winner)
            break
        if player == 1:
            next_move(board)
        else:
            pos = list(map(int, input('Position: ').split()))
            board.place(pos, 2)
        player = int(not (player - 1)) + 1

        print(board.board)


from models.board import Board

if __name__ == '__main__':
    board = Board()
    play(board)
