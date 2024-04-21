import pygame

from search_game import constants, draw_grid, pathfinder
from search_game.global_state import GLOBAL_STATE

init_callbacks = [draw_grid.init, pathfinder.init]


def main():
    pygame.init()
    pygame.display.set_caption(constants.INITIAL_WINDOW_CAPTION)
    constants.init()

    GLOBAL_STATE.init(
        init_callbacks=init_callbacks,
        main_loop=pathfinder.DRAW_LOOP,
    )

    while GLOBAL_STATE.running:
        GLOBAL_STATE.update()

    pygame.quit()
