from typing import override

import pygame

from search_game.constants import (
    DEFAULT_COLOR_PALLETTE,
    GRID_SCALE,
    PATH_COLOR,
    WALL_COLOR,
    render_text,
)
from search_game.gameobject import GameObject
from search_game.global_state import GLOBAL_STATE
from search_game.renderable import Renderable, RenderLayer

placement_color = PATH_COLOR

DEFAULT_PLACEMENT_COLOR_UI_POS = (20, 20)
DEFAULT_PLACEMENT_COLOR_UI_TEXT = "Current Placement Color:"
DEFAULT_PLACEMENT_COLOR_OFFSET = (10, 2)
DEFAULT_PALLETE_MARGIN = GRID_SCALE // 2
DEFAULT_PLACEMENT_COLOR_PALETTE_UI_POS = (400, 20)
DEFAULT_PLACEMENT_COLOR_PALETTE_UI_TEXT = "Color Palette:"


class CurrentPlacementColorDisplay(Renderable):
    pos: tuple[int, int]
    rect: pygame.Rect
    text_surface: pygame.Surface

    def __init__(
        self, pos: tuple[int, int], text_surface: pygame.Surface, rect: pygame.Rect
    ):
        self.pos = pos
        self.text_surface = text_surface
        self.rect = rect

    @override
    def render(self, screen: pygame.Surface):
        screen.blit(self.text_surface, self.pos)
        pygame.draw.rect(screen, placement_color, self.rect)

    @staticmethod
    def default():
        text_surface = render_text(DEFAULT_PLACEMENT_COLOR_UI_TEXT)
        left = (
            DEFAULT_PLACEMENT_COLOR_UI_POS[0]
            + text_surface.get_width()
            + DEFAULT_PLACEMENT_COLOR_OFFSET[0]
        )
        top = DEFAULT_PLACEMENT_COLOR_UI_POS[1] + DEFAULT_PLACEMENT_COLOR_OFFSET[1]
        rect = pygame.Rect(
            left,
            top,
            GRID_SCALE,
            GRID_SCALE,
        )
        return CurrentPlacementColorDisplay(
            DEFAULT_PLACEMENT_COLOR_UI_POS, text_surface, rect
        )


class PlacementColorPalette(Renderable, GameObject):
    colors: list[pygame.Color]
    rects: list[pygame.Rect]
    text_surface: pygame.Surface

    def render(self, screen: pygame.Surface):
        screen.blit(self.text_surface, DEFAULT_PLACEMENT_COLOR_PALETTE_UI_POS)
        for rect, color in zip(self.rects, self.colors):
            pygame.draw.rect(screen, color, rect)

    def update(self):
        if not GLOBAL_STATE.any_event(pygame.MOUSEBUTTONDOWN):
            return
        mouse_presses = pygame.mouse.get_pressed()
        if not mouse_presses[0]:
            return  # only handle left mouse button
        pos = pygame.mouse.get_pos()
        for rect, color in zip(self.rects, self.colors):
            if rect.collidepoint(pos):
                global placement_color
                placement_color = color

    def __init__(
        self,
        colors: list[pygame.Color],
        pos: tuple[int, int],
        text_surface: pygame.Surface,
    ):
        self.colors = colors
        self.text_surface = text_surface
        self.rects = list(
            map(
                lambda x: pygame.Rect(
                    pos[0]
                    + text_surface.get_width()
                    + DEFAULT_PLACEMENT_COLOR_OFFSET[0]
                    + x * (GRID_SCALE + DEFAULT_PALLETE_MARGIN),
                    pos[1] + DEFAULT_PLACEMENT_COLOR_OFFSET[1],
                    GRID_SCALE,
                    GRID_SCALE,
                ),
                range(len(colors)),
            )
        )

    @staticmethod
    def default() -> "PlacementColorPalette":
        text_surface = render_text(DEFAULT_PLACEMENT_COLOR_PALETTE_UI_TEXT)
        return PlacementColorPalette(
            DEFAULT_COLOR_PALLETTE, DEFAULT_PLACEMENT_COLOR_PALETTE_UI_POS, text_surface
        )


def init():
    default_placement_color_ui = CurrentPlacementColorDisplay.default()
    default_color_palette_ui = PlacementColorPalette.default()
    GLOBAL_STATE.game_objects.append(default_color_palette_ui)
    GLOBAL_STATE.renderdict[RenderLayer.UI].extend(
        [default_placement_color_ui, default_color_palette_ui]
    )


def handle_left_mouse():
    pos = pygame.mouse.get_pos()
    pos = pygame.Vector2(pos)
    grid_pos = GLOBAL_STATE.grid.screen_to_grid(pos)
    if grid_pos is None:
        return
    GLOBAL_STATE.grid.place_square(*grid_pos, placement_color)


def handle_right_mouse():
    pos = pygame.mouse.get_pos()
    pos = pygame.Vector2(pos)
    grid_pos = GLOBAL_STATE.grid.screen_to_grid(pos)
    if grid_pos is None:
        return
    GLOBAL_STATE.grid.place_square(*grid_pos, WALL_COLOR)


def create_grid_loop():
    # mouse buttons in order of (left, wheel, right)
    pressed_tuple = pygame.mouse.get_pressed()

    if pressed_tuple[0]:
        handle_left_mouse()
    if pressed_tuple[2]:
        handle_right_mouse()
