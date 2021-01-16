from tensorflow import keras
import numpy as np
import random
from collections import deque
from strategies.heuristic import Heuristic
from models.board import Board
from strategies.utils import reverse_players
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class Agent:
    def __init__(self, gamma=0.0, max_gamma=0.9, epsilon=1.0, min_epsilon=0.1, max_replay_buffer_size=5000, size=15,
                 model=None, name='agent'):

        self.model = model or keras.Sequential([
            keras.Input(shape=(size, size, 1)),
            keras.layers.Conv2D(32, (6, 6), activation='relu'),
            keras.layers.Conv2D(32, (5, 5), activation='relu'),
            keras.layers.Flatten(),
            keras.layers.Dense(200, activation='relu'),
            keras.layers.Dense(100, activation='relu'),
            keras.layers.Dense(size*2)
        ])
        self.model.compile(optimizer=keras.optimizers.Adam(), loss="mse", metrics=["mse"])
        self.name = name
        self.size = size
        self.replay_buffer = deque()
        self.max_replay_buffer_size = max_replay_buffer_size
        self.gamma = gamma
        self.max_gamma = max_gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon

    @staticmethod
    def random_flip_rotate(board1, board2):
        values1 = [np.rot90(board1.copy()) for _ in range(3)] + [np.flip(board1.copy(), i) for i in range(2)]
        values2 = [np.rot90(board2.copy()) for _ in range(3)] + [np.flip(board2.copy(), i) for i in range(2)]

        return random.sample(list(zip(values1, values2)), random.randint(0, len(values1)))

    def _reward(self, board, winner):
        if winner == 1:
            return self.size * self.size * 2 - len(np.where(board == 1)[0])
        elif winner == 2:
            return -self.size * self.size * 2
        return 1

    def play(self, board, player):
        if player == 1:
            q_moves = self.prediction(board.board)
        elif player == 2:
            q_moves = self.prediction(reverse_players(board.board))

        i, j = np.argmax(q_moves[:self.size]), np.argmax(q_moves[self.size:])
        if board.board[i, j] == Board.EMPTY_CELL:
            board.place((i, j), player)
        else:
            board.place(random.choice(np.argwhere(board.board == Board.EMPTY_CELL)), player)

    def _add_to_replay_buffer(self, episodes, max_game_states):
        for ep in range(episodes):
            board = Board(self.size)
            heuristic = Heuristic(2)
            bad_move = False
            for _ in range(max_game_states):
                st = board.copy()
                q_moves = self.prediction(st.board)

                if np.random.rand() < self.epsilon:
                    move = np.random.randint(0, self.size, 2)
                else:
                    move = np.argmax(q_moves[:self.size]), np.argmax(q_moves[self.size:])
                if board.board[tuple(move)]:
                    reward = -self.size * self.size
                    bad_move = True
                else:
                    board.place(move, 1)
                    winner = board.is_finished()
                    if not winner:
                        heuristic.next_move(board)

                        # self.play(board, 2)  # RN VS RN

                        # board.place(random.choice(np.argwhere(board.board == 0)), 2)  # RN VS RANDOM
                    reward = self._reward(board.board, winner)

                for st_group in Agent.random_flip_rotate(st.board, board.board) + [(st.board, board.board.copy())]:
                    if len(self.replay_buffer) == self.max_replay_buffer_size:
                        self.replay_buffer.popleft()
                    self.replay_buffer.append((st_group[0], q_moves, move, reward, st_group[1]))

                if board.is_finished() or bad_move:
                    break

            if self.epsilon > self.min_epsilon:
                self.epsilon -= 0.0005
            if self.gamma < self.max_gamma:
                self.gamma += 0.001

    def train(self, episodes, epochs, batch_size, nr_episodes_between_games):
        for _ in range(episodes//nr_episodes_between_games):
            self._add_to_replay_buffer(nr_episodes_between_games, 180)
            print(len(self.replay_buffer), batch_size)
            sample_size = min(batch_size, len(self.replay_buffer))
            batch = random.sample(self.replay_buffer, sample_size)
            train_feature = np.zeros(shape=(sample_size, self.size, self.size), dtype=np.uint8)
            train_label = np.zeros(shape=(sample_size, self.size*2), dtype=np.float)

            batch_st_next_state = np.array([experience[4] for experience in batch])
            batch_predict_next_state = self.prediction(np.array(batch_st_next_state))
            for i, experience in enumerate(batch):
                train_feature[i] = experience[0]  # current state
                train_label[i] = experience[1]  # predicted values by RN

                q_moves_next_state = batch_predict_next_state[i]

                next_move = np.argmax(q_moves_next_state[:self.size]), np.argmax(q_moves_next_state[self.size:])

                current_move, reward = experience[2:4]
                train_label[i][current_move[0]] = reward + self.gamma * q_moves_next_state[next_move[0]]
                train_label[i][current_move[1] + self.size] = reward + self.gamma * q_moves_next_state[next_move[1]]

            self.model.fit(train_feature[:, :, :, None], train_label, batch_size//4, epochs, validation_split=0.2)
            if _ % 500 == 0:
                self.save_model(f'{self.name}_{_}')

    def prediction(self, states):
        if len(states.shape) == 2:
            return self.model(states[None, :, :, None], training=False)[0]
        return self.model.predict(states[:, :, :, None])

    def save_model(self, path):
        self.model.save(filepath=path)


if __name__ == '__main__':
    agent_A = Agent(gamma=0, max_gamma=0.99, max_replay_buffer_size=50000, name='agent_Adrian_jr')
    agent_A.train(8000000, 10, 5000, 5)

    agent_A.save_model(agent_A.name)
