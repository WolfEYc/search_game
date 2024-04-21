import pygame

from search_game import constants, draw_grid
from search_game.global_state import GLOBAL_STATE


def quit():
    GLOBAL_STATE.running = False


def quit_game_if_event():
    if GLOBAL_STATE.any_event(pygame.QUIT):
        quit()


def render_bg():
    GLOBAL_STATE.screen.fill(GLOBAL_STATE.background_color)


def render_objects():
    for _, render_list in GLOBAL_STATE.renderdict.items():
        for renderable in render_list:
            renderable.render(GLOBAL_STATE.screen)


main_loop = [
    quit_game_if_event,
    render_bg,
    draw_grid.create_grid_loop,
    render_objects,
]

init_callbacks = [draw_grid.init]


def main():
    pygame.init()
    pygame.display.set_caption(constants.INITIAL_WINDOW_CAPTION)
    constants.init()

    GLOBAL_STATE.init(init_callbacks=init_callbacks, main_loop=main_loop)

    while GLOBAL_STATE.running:
        GLOBAL_STATE.update()

    pygame.quit()
