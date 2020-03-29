import pygame
import sys
from modules import CONST

def terminate():
    pygame.quit()
    sys.exit()

pygame.init()
screen = pygame.display.set_mode(CONST.SIZE)
running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            terminate()
