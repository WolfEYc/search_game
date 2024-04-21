from typing import Callable

import pygame

from search_game.constants import (
    CLOCK,
    DEFAULT_FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WALL_COLOR,
)
from search_game.gameobject import GameObject
from search_game.grid import Grid
from search_game.renderable import RenderDict, RenderLayer, generate_renderable_list


class GlobalState:
    background_color: pygame.Color
    running: bool
    init_callbacks: list[Callable]
    main_loop: list[Callable]
    game_objects: list[GameObject]
    screen: pygame.Surface
    renderdict: RenderDict
    grid: Grid
    dt: float
    events: list[pygame.event.Event]

    def init(self, init_callbacks: list[Callable] = [], main_loop: list[Callable] = []):
        self.grid = Grid.default()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_color = WALL_COLOR
        self.running = True
        self.init_callbacks = init_callbacks
        self.main_loop = main_loop
        self.renderdict = generate_renderable_list()
        self.renderdict[RenderLayer.GRID] = [self.grid]
        self.dt = 0
        self.events = []
        self.game_objects = []

        for callback in self.init_callbacks:
            callback()

    def update(self):
        self.events = pygame.event.get()
        for callback in self.main_loop:
            callback()

        for game_object in self.game_objects:
            game_object.update()

        pygame.display.flip()
        self.dt = CLOCK.tick(DEFAULT_FPS) / 1000

    def any_event(self, event_type: int) -> bool:
        return any(event.type == event_type for event in self.events)


GLOBAL_STATE = GlobalState()
