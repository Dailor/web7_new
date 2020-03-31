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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # MousePgUp = 4 and MousePgDown = 5
            if event.button == 4:
                app.change_scale(CONST.UP_SCALE)
            elif event.button == 5:
                app.change_scale(CONST.DOWN_SCALE)


        elif event.type == pygame.KEYDOWN:
            # Keyboard PgUp and PgDown
            if event.key == pygame.K_PAGEDOWN:
                app.change_scale(CONST.DOWN_SCALE)
            elif event.key == pygame.K_PAGEUP:
                app.change_scale(CONST.UP_SCALE)

            #Перемещение по карте
            elif event.key == pygame.K_UP:
                app.change_coords(CONST.MOVE_UP)
            elif event.key == pygame.K_DOWN:
                app.change_coords(CONST.MOVE_DOWN)
            elif event.key == pygame.K_LEFT:
                app.change_coords(CONST.MOVE_LEFT)
            elif event.key == pygame.K_RIGHT:
                app.change_coords(CONST.MOVE_RIGHT)

    screen.fill((0, 0, 0))
    app.render()
    pygame.display.flip()
