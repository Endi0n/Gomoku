from views.gomoku import GomokuView
from views.game import Game
from models.board import Board
import strategies
import globals


class MenuStart(GomokuView):

    def __init__(self, screen):
        super().__init__(screen)
        self.size = None

        self.start_selected()

    def start_selected(self):

        self.add_button('15 x 15', 16,
                        (255, 255, 255), (70, 70, 70),
                        (globals.WIDTH // 2, 180),
                        (globals.WIDTH // 4 * 3, 30),
                        self.board_size_selected(15))

        self.add_button('19 x 19', 16,
                        (255, 255, 255), (70, 70, 70),
                        (globals.WIDTH // 2, 220),
                        (globals.WIDTH // 4 * 3, 30),
                        self.board_size_selected(19))

    def board_size_selected(self, size):
        def closure():
            self.size = size

            self.buttons = []
            globals.GAME_VIEW = None

            algorithms = ['Heuristic', 'AB Pruning', 'MTSC', 'Neural Network']

            for x, algorithm in enumerate(algorithms):
                self.add_button(algorithm, 16,
                                (255, 255, 255), (70, 70, 70),
                                (globals.WIDTH // 2, 180 + 40 * x),
                                (globals.WIDTH // 4 * 3, 30),
                                self.algorithm_selected(algorithm))

            self.add_button('Back', 16,
                            (255, 255, 255), (70, 70, 70),
                            (globals.WIDTH // 2, globals.HEIGHT - 50),
                            (globals.WIDTH // 4 * 3, 30),
                            self.back_selected)

        return closure

    def back_selected(self):
        self.buttons = []
        self.start_selected()

    def algorithm_selected(self, algorithm):
        def closure():
            if algorithm == 'Heuristic':
                globals.strategy = strategies.Heuristic(1)
            elif algorithm == 'AB Pruning':
                globals.strategy = strategies.AbPruning(1)
            elif algorithm == 'MTSC':
                globals.strategy = strategies.MonteCarloTreeSearch(1)
            elif algorithm == 'Neural Network':
                globals.strategy = strategies.NeuralNetwork(1)
            if not globals.GAME_VIEW or globals.GAME_VIEW.board.is_finished():
                globals.GAME_VIEW = Game(self.screen, Board(size=self.size))

            globals.CURRENT_VIEW = globals.GAME_VIEW

        return closure

    def render(self):
        super().render()

        if not self.size:
            self.write('Chose the board size:', 18, (globals.WIDTH / 2, 110), (0, 0, 0), center=True, font_name='arial')
        else:
            self.write('Chose the opposing algorithm:', 18, (globals.WIDTH / 2, 110), (0, 0, 0), center=True, font_name='arial')

        self.render_buttons()
        #
        # if self.pressed:
        #     self.fill((255, 255, 255))
