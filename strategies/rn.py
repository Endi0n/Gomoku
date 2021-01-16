from strategies.strategy import Strategy
from strategies.qlearning_agent import Agent
from tensorflow import keras


class NeuralNetwork(Strategy):
    def __init__(self, player):
        self.player = player
        self.agent = Agent(model=keras.models.load_model('strategies/agent_Adrian_jr'))

    def next_move(self, board):
        self.agent.play(board, self.player)
