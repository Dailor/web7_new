import pygame
import sys
from modules import CONST
from modules.App import App
from modules.Button import ButtonGroupOfGroups


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()

screen = pygame.display.set_mode(CONST.SIZE)
group_of_groups = dict()

buttons_group_of_groups = ButtonGroupOfGroups()

group_of_groups['btn'] = buttons_group_of_groups

app = App(screen, group_of_groups)
running = True
while running:
    for event in pygame.event.get():

        if (event.type == pygame.QUIT):
            terminate()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                buttons_group_of_groups.check_release()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                buttons_group_of_groups.check_press(event.pos)

            # MousePgUp = 4 and MousePgDown = 5
            elif event.button == 4:
                app.change_scale(CONST.UP_SCALE)
            elif event.button == 5:
                app.change_scale(CONST.DOWN_SCALE)


        elif event.type == pygame.KEYDOWN:
            # Keyboard PgUp and PgDown
            if event.key == pygame.K_PAGEDOWN:
                app.change_scale(CONST.DOWN_SCALE)
            elif event.key == pygame.K_PAGEUP:
                app.change_scale(CONST.UP_SCALE)

            # Перемещение по карте
            elif event.key == pygame.K_UP:
                app.change_coords(CONST.MOVE_UP)
            elif event.key == pygame.K_DOWN:
                app.change_coords(CONST.MOVE_DOWN)
            elif event.key == pygame.K_LEFT:
                app.change_coords(CONST.MOVE_LEFT)
            elif event.key == pygame.K_RIGHT:
                app.change_coords(CONST.MOVE_RIGHT)

    screen.fill(CONST.BG_COLOR)
    app.render()
    pygame.display.flip()
