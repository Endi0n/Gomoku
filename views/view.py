from abc import ABC, abstractmethod
import pygame


class View(ABC):
    fonts = {}

    def __init__(self, screen):
        self.screen = screen

    @abstractmethod
    def render(self):
        pass

    def write(self, text, size, color, position, font_name='timesnewroman', center=False):
        font = View.load_font(font_name, size)
        text_surface = font.render(text, True, color)

        if center:
            text_rect = text_surface.get_rect()
            text_rect.center = position
            position = text_rect

        self.screen.blit(text_surface, position)

    def fill(self, color):
        self.screen.fill(color)

    @staticmethod
    def load_font(font, size):
        if (font, size) not in View.fonts:
            View.fonts[(font, size)] = pygame.font.SysFont(font, size)
        return View.fonts[(font, size)]
