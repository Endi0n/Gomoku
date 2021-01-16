import abc


class Strategy(abc.ABC):

    @abc.abstractmethod
    def next_move(self, board):
        pass

