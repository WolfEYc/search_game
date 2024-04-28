import pygame

from search_game import draw_grid
from search_game.bfs_isaac import bfs_isaac
from search_game.clock import Ticker
from search_game.constants import PATHFIND_TICK
from search_game.global_state import GLOBAL_STATE, Gamemode

pathfind_ticker = Ticker(PATHFIND_TICK)

clock = pygame.time.Clock()
pathfind_counter = 0
# change out the bfs implementation here
bfs_implementation = bfs_isaac


def pathfind_update():
    global pathfind_counter
    if not pathfind_ticker.tick():
        return
    if GLOBAL_STATE.grid.found_path is not None:
        return

    GLOBAL_STATE.grid.found_path = bfs_implementation(GLOBAL_STATE.grid)
    print("pathfind tick ", pathfind_counter)
    pathfind_counter += 1

    if GLOBAL_STATE.grid.found_path is None:
        return

    print("Path found!")


def pathfind_toggle():
    global pathfind_counter
    if GLOBAL_STATE.key_event(pygame.KEYDOWN, pygame.K_SPACE):
        print("Toggling pathfind")
        pathfind_counter = 0

        if GLOBAL_STATE.gamemode == Gamemode.PLAY:
            GLOBAL_STATE.set_gamemode(Gamemode.DRAW, DRAW_LOOP)
        else:
            GLOBAL_STATE.set_gamemode(Gamemode.PLAY, PATHFIND_LOOP)


def init():
    pass


DRAW_LOOP = [draw_grid.create_grid_loop, pathfind_toggle]
PATHFIND_LOOP = [pathfind_update, pathfind_toggle]
