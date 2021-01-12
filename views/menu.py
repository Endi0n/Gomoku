from views.gomoku import GomokuView
import globals


class Menu(GomokuView):

    def __init__(self, screen):
        super(Menu, self).__init__(screen)

        self.pressed = False
        self.add_button('Make screen white', 16,
                        (255, 255, 255), (70, 70, 70),
                        (globals.WIDTH // 2, 120),
                        (globals.WIDTH // 4 * 3, 30),
                        self.test_btn_pressed)

        self.add_button('Print Hello on console', 16,
                        (255, 255, 255), (70, 70, 70),
                        (globals.WIDTH // 2, 160),
                        (globals.WIDTH // 4 * 3, 30),
                        self.test2_btn_pressed)

    def test_btn_pressed(self):
        self.pressed = True

    def test2_btn_pressed(self):
        print('Hello')

    def render(self):
        super().render()

        self.render_buttons()

        if self.pressed:
            self.fill((255, 255, 255))
