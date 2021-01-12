from abc import ABC, abstractmethod
import pygame


class View(ABC):
    fonts = {}

    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for btn in self.buttons:
            position, size = btn[0]
            if position[0] <= mouse_x <= position[0] + size[0] \
                    and position[1] <= mouse_y <= position[1] + size[1]:
                btn[-1]()
                return

    def fill(self, color):
        self.screen.fill(color)

    @staticmethod
    def load_font(font, size):
        if (font, size) not in View.fonts:
            View.fonts[(font, size)] = pygame.font.SysFont(font, size)
        return View.fonts[(font, size)]

    def write(self, text, size, color, position, font_name='timesnewroman', center=False):
        font = View.load_font(font_name, size)
        text_surface = font.render(text, True, color)

        if center:
            text_rect = text_surface.get_rect()
            text_rect.center = position
            position = text_rect

        self.screen.blit(text_surface, position)

    def add_button(self, text, text_size, fg_color, bg_color, position, size, callback, font_name='timesnewroman'):
        font = View.load_font(font_name, text_size)
        text_surface = font.render(text, True, fg_color)

        text_rect = text_surface.get_rect()
        text_rect.center = position

        position = (position[0] - size[0] // 2, position[1] - size[1] // 2)

        self.buttons.append(((position, size), (text_surface, text_rect, bg_color), callback))

    def render_buttons(self):
        for btn in self.buttons:
            pygame.draw.rect(self.screen, btn[1][-1], pygame.Rect(btn[0]))
            self.screen.blit(btn[1][0], btn[1][1])

    @abstractmethod
    def render(self):
        pass
