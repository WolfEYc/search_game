import pygame

from search_game import draw_grid
from search_game.clock import Ticker
from search_game.constants import PATHFIND_TICK
from search_game.global_state import GLOBAL_STATE, Gamemode

pathfind_ticker = Ticker(PATHFIND_TICK)

clock = pygame.time.Clock()


def pathfind_update():
    if not pathfind_ticker.tick():
        return
    print("Pathfinding update")


def pathfind_toggle():
    global pathfinding
    if GLOBAL_STATE.key_event(pygame.KEYDOWN, pygame.K_SPACE):
        print("Toggling pathfind")

        if GLOBAL_STATE.gamemode == Gamemode.PLAY:
            GLOBAL_STATE.set_gamemode(Gamemode.DRAW, DRAW_LOOP)
        else:
            GLOBAL_STATE.set_gamemode(Gamemode.PLAY, PATHFIND_LOOP)


def init():
    pass


DRAW_LOOP = [draw_grid.create_grid_loop, pathfind_toggle]
PATHFIND_LOOP = [pathfind_update, pathfind_toggle]
