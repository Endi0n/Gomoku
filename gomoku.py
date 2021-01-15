import globals
import pygame
import sys


# Window initialization
pygame.display.set_caption('Gomoku')

# Initial render
globals.CURRENT_VIEW.render()
pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        globals.CURRENT_VIEW.handle_event(event)

    globals.CURRENT_VIEW.render()
    pygame.display.flip()

sys.exit()
