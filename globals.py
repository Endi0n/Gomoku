import pygame
import views

WIDTH = 500
HEIGHT = 500

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
MENU_VIEW = views.Menu(SCREEN)

CURRENT_VIEW = MENU_VIEW
