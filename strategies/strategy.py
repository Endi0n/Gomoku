import abc


class Strategy(abc.ABC):

    @abc.abstractmethod
    def next_move(self, board, player):
        pass

