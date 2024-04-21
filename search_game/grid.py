from math import floor
from typing import Optional

import numpy as np
import pygame

from search_game.constants import (
    COLORS,
    END_COLOR,
    GRID_LEFT,
    GRID_SCALE,
    GRID_TOP,
    PATH_COLOR,
    SCREEN_WIDTH,
    START_COLOR,
)
from search_game.renderable import Renderable


class Grid(Renderable):
    grid: np.ndarray
    scale: int
    grid_width: int
    grid_height: int
    bounding_box: pygame.Rect
    start_point: Optional[tuple[int, int]]
    end_point: Optional[tuple[int, int]]

    def __init__(self, scale: int, bounding_box: pygame.Rect):
        self.scale = scale
        self.bounding_box = bounding_box
        grid_size = pygame.Vector2(bounding_box.size) // scale
        self.grid_width = floor(grid_size.x)
        self.grid_height = floor(grid_size.y)
        self.start_point = None
        self.end_point = None

        self.grid = np.zeros(
            shape=(self.grid_width, self.grid_height, COLORS), dtype=np.uint8
        )

    def screen_to_grid(self, mouse_pos: pygame.Vector2):
        if not self.bounding_box.collidepoint(*mouse_pos):
            return None

        grid_pos = (mouse_pos - self.bounding_box.topleft) // self.scale
        grid_x = floor(grid_pos.x)
        grid_y = floor(grid_pos.y)

        return (grid_x, grid_y)

    def place_square(self, grid_x: int, grid_y: int, color: pygame.Color):
        grid_tuple = (grid_x, grid_y)
        if color == START_COLOR and self.start_point:
            self.grid[self.start_point] = PATH_COLOR

        if color == END_COLOR and self.end_point:
            self.grid[self.end_point] = PATH_COLOR

        if color != START_COLOR and self.start_point == grid_tuple:
            self.start_point = None

        if color != END_COLOR and self.end_point == grid_tuple:
            self.end_point = None

        if color == START_COLOR:
            self.start_point = grid_tuple

        if color == END_COLOR:
            self.end_point = grid_tuple

        self.grid[grid_tuple] = color
        print(f"{self.start_point=}, {self.end_point=}")

    def render(self, screen: pygame.Surface):
        offset_x, offset_y = self.bounding_box.topleft
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                color = self.grid[x, y]
                pixel_x = x * self.scale + offset_x
                pixel_y = y * self.scale + offset_y
                rect = pygame.Rect(pixel_x, pixel_y, self.scale, self.scale)
                pygame.draw.rect(screen, color=color, rect=rect)

    @staticmethod
    def default() -> "Grid":
        bounding_box = pygame.Rect(GRID_LEFT, GRID_TOP, SCREEN_WIDTH, SCREEN_WIDTH)
        return Grid(scale=GRID_SCALE, bounding_box=bounding_box)
