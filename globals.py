import pygame
import views
from models.board import Board

WIDTH = 532
HEIGHT = 582

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

MENU_VIEW = views.Menu(SCREEN)
GAME_VIEW = views.Game(SCREEN, Board(size=15))

CURRENT_VIEW = GAME_VIEW
