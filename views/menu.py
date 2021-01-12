from views.gomoku import GomokuView
import globals


class Menu(GomokuView):

    def setup(self):
        self.add_button('Test', 16,
                        (255, 255, 255), (70, 70, 70),
                        (globals.WIDTH // 2, 120),
                        (globals.WIDTH // 4 * 3, 30),
                        None)


