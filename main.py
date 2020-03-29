import pygame
import sys
from modules import CONST
from modules.App import App


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
screen = pygame.display.set_mode(CONST.SIZE)
app = App(screen)
running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # PgUp = 4 and PgDown = 5
            if event.button == 4 or event.button == 5:
                app.change_scale(event.button)
    screen.fill((0, 0, 0))
    app.render()
    pygame.display.flip()
