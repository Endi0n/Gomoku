from views.gomoku import GomokuView
import globals
from threading import Thread


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

        self.computer_turn = False
        self.finished = None

        self.thread = Thread(target=self.computer_move, daemon=True)
        self.thread.start()

        self.add_button('Back', 14,
                        (255, 255, 255), (70, 70, 70),
                        (globals.WIDTH // 2, globals.HEIGHT - 25),
                        (globals.WIDTH // 4, 20),
                        self.back_selected)


    def back_selected(self):
        globals.CURRENT_VIEW = globals.MENU_VIEW

    def computer_move(self):
        while True:
            while not self.computer_turn and self.finished is None:
                continue
            if self.finished is not None:
                return
            globals.strategy.next_move(self.board)
            self.computer_turn = False
            self.finished = self.board.is_finished()

    def handle_click(self, position):
        super().handle_click(position)

        if self.computer_turn:
            return

        if self.finished is not None:
            return

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

        self.finished = self.board.is_finished()
        self.computer_turn = True

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

    def render_status(self):
        if self.finished is None:
            self.draw_circle(10, (60, 50), (255, 255, 255) if self.computer_turn else (0, 0, 0))
            self.write('moves', 15, (100, 50), (0, 0, 0), center=True)
        else:
            self.draw_circle(10, (60, 50), (255, 255, 255) if not self.computer_turn else (0, 0, 0))
            self.write('won', 15, (100, 50), (0, 0, 0), center=True)

            if self.thread:
                self.thread.join()
                self.thread = None

    def render(self):
        super().render()

        self.render_board()
        self.render_pieces()
        self.render_indexes()
        self.render_status()

        self.render_buttons()
