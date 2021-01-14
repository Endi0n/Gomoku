from views.gomoku import GomokuView
import globals


class Game(GomokuView):
    PADDING_VERTICAL = 50
    PADDING_TOP = 50
    PADDING_BOTTOM = 50
    SPACE = 24

    def __init__(self, screen, board):
        super().__init__(screen)
        self.board = board

    def render(self):
        super().render()

        size = self.board.size - 1
        space = Game.SPACE

        vertical = (globals.WIDTH - size * space) // 2
        assert (vertical >= Game.PADDING_VERTICAL)

        horizontal = (globals.HEIGHT - size * space - Game.PADDING_TOP) // 2
        assert (horizontal >= Game.PADDING_BOTTOM)

        top = Game.PADDING_TOP

        for x in range(self.board.size):
            self.draw_line((vertical + x * space, top + horizontal),
                           (vertical + x * space, globals.HEIGHT - horizontal),
                           1, (0, 0, 0))

            self.draw_line((vertical, top + horizontal + x * space),
                           (globals.WIDTH - vertical, top + horizontal + x * space),
                           1, (0, 0, 0))
