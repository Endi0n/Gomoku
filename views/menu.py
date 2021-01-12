from .view import View
import globals


class Menu(View):

    def render(self):
        self.fill((200, 200, 200))

        self.write('Gomoku', 30, (0, 0, 255), (globals.WIDTH // 2, 30), center=True)
