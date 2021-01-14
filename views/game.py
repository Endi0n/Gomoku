from views.gomoku import GomokuView
from strategies.heuristic import next_move
import globals


class Game(GomokuView):
    PADDING_VERTICAL = 50
    PADDING_TOP = 50
    PADDING_BOTTOM = 50
    SPACE = 24

    def __init__(self, screen, board):
        super().__init__(screen)
        self.board = board

        size = self.board.size - 1

        if self.board.size == 15:
            self.space = 30
        else:
            self.space = Game.SPACE

        self.vertical = (globals.WIDTH - size * self.space) // 2
        assert (self.vertical >= Game.PADDING_VERTICAL)

        self.horizontal = (globals.HEIGHT - size * self.space - Game.PADDING_TOP) // 2
        assert (self.horizontal >= Game.PADDING_BOTTOM)

        self.top = Game.PADDING_TOP

    def handle_click(self, position):
        super().handle_click(position)

        pos_x, pos_y = position

        if not (self.vertical - self.space // 2 <= pos_x <= globals.WIDTH - self.vertical + self.space // 2
                and self.horizontal + Game.PADDING_TOP - self.space // 2 <= pos_y <= globals.HEIGHT - self.horizontal
                + self.space // 2):
            return

        pos_x -= self.vertical
        pos_y -= self.top + self.horizontal

        pos_x /= self.space
        pos_y /= self.space

        pos_x, pos_y = int(round(pos_x)), int(round(pos_y))

        self.board.board[pos_x][pos_y] = 2
        next_move(self.board)

        print(self.board.is_finished())


    def render_board(self):
        for x in range(self.board.size):
            self.draw_line((self.vertical + x * self.space, self.top + self.horizontal),
                           (self.vertical + x * self.space, globals.HEIGHT - self.horizontal),
                           1, (0, 0, 0))

            self.draw_line((self.vertical, self.top + self.horizontal + x * self.space),
                           (globals.WIDTH - self.vertical, self.top + self.horizontal + x * self.space),
                           1, (0, 0, 0))

    def render_indexes(self):
        for x in range(self.board.size):
            self.write(str(x), 10, (self.vertical + x * self.space, self.top + self.horizontal - 10), (0, 0, 0), center=True)

            self.write(str(x), 10, (self.vertical - 10, self.top + self.horizontal + x * self.space), (0, 0, 0), center=True)

    def render_pieces(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] == 0:
                    continue

                player1 = self.board.board[i][j] == 1

                self.draw_circle(self.space // 2 - 2,
                                 (self.vertical + i * self.space,
                                  self.top + self.horizontal + j * self.space),
                                 (255, 255, 255) if player1 else (0, 0, 0))

    def render(self):
        super().render()

        self.render_board()
        self.render_pieces()
        self.render_indexes()
