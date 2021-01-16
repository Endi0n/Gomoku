import pygame
import views
from models.board import Board
from strategies.heuristic import Heuristic

WIDTH = 532
HEIGHT = 582

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

MENU_VIEW = views.MenuStart(SCREEN)
GAME_VIEW = None

CURRENT_VIEW = MENU_VIEW

strategy = None

