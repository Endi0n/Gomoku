from .view import View
import globals


class GomokuView(View):
    def render(self):
        self.fill((200, 200, 200))

        self.write('Gomoku', 30, (0, 0, 255), (globals.WIDTH // 2, 50), center=True)
