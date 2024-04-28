from enum import Enum
from typing import Callable, Iterable

import pygame

from search_game import gameglobals
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


class Gamemode(Enum):
    DRAW = 0
    PLAY = 1


class GlobalState:
    background_color: pygame.Color
    running: bool
    init_callbacks: list[Callable]
    main_loop: list[Callable]
    game_objects: list[GameObject]
    screen: pygame.Surface
    renderdict: RenderDict
    grid: Grid
    events: list[pygame.event.Event]
    gamemode: Gamemode

    def init(
        self,
        init_callbacks: list[Callable] = [],
        main_loop: list[Callable] = [],
        gamemode: Gamemode = Gamemode.DRAW,
    ):
        self.grid = Grid.default()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_color = WALL_COLOR
        self.running = True
        self.init_callbacks = init_callbacks
        self.main_loop = main_loop
        self.renderdict = generate_renderable_list()
        self.renderdict[RenderLayer.GRID] = [self.grid]
        self.events = []
        self.game_objects = []
        self.gamemode = gamemode

        for callback in self.init_callbacks:
            callback()

    def quit(self):
        self.running = False

    def quit_game_if_event(self):
        if self.any_event(pygame.QUIT):
            quit()

    def render_bg(self):
        self.screen.fill(self.background_color)

    def render_objects(self):
        for _, render_list in self.renderdict.items():
            for renderable in render_list:
                renderable.render(self.screen)

    def update(self):
        self.events = pygame.event.get()

        self.quit_game_if_event()
        self.render_bg()
        for callable in self.main_loop:
            callable()

        for game_object in self.game_objects:
            game_object.update()

        self.render_objects()

        pygame.display.flip()
        gameglobals.dt = CLOCK.tick(DEFAULT_FPS) / 1000

    def filter_events(self, event_type: int) -> Iterable[pygame.event.Event]:
        filtered_events = filter(lambda e: e.type == event_type, self.events)
        return filtered_events

    def any_event(self, event_type: int) -> bool:
        return any(event.type == event_type for event in self.events)

    def key_event(self, event_type: int, key_code: int) -> bool:
        filtered_events = self.filter_events(event_type)
        return any(e.type == event_type and e.key == key_code for e in filtered_events)

    def set_gamemode(self, gamemode: Gamemode, loop: list[Callable]):
        self.grid.reset_path()

        if gamemode == Gamemode.PLAY:
            if not self.grid.is_ready():
                return
            self.grid.init_queue()

        self.gamemode = gamemode
        self.main_loop = loop


GLOBAL_STATE = GlobalState()
