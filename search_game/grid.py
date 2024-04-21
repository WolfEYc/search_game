from enum import Enum
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
    VISITED_COLOR,
    WALL_COLOR,
)
from search_game.renderable import Renderable


class CellState(Enum):
    Wall = 0
    Path = 1
    Visited = 2
    Start = 3
    End = 4

    @staticmethod
    def from_color(color: np.ndarray) -> "CellState":
        pygame_color = pygame.Color(color[0], color[1], color[2], color[3])
        if pygame_color == START_COLOR:
            return CellState.Start
        if pygame_color == END_COLOR:
            return CellState.End
        if pygame_color == PATH_COLOR:
            return CellState.Path
        if pygame_color == WALL_COLOR:
            return CellState.Wall
        raise ValueError(f"Unknown grid color: {pygame_color}")


def draw_arrow(
    screen: pygame.Surface,
    color: pygame.Color,
    start_pos: pygame.Vector2,
    end_pos: pygame.Vector2,
    width: int = 2,
):
    # draw the inital line
    pygame.draw.line(screen, color, start_pos, end_pos, width)

    angle = start_pos.angle_to(end_pos)
    normalized_start_pos = start_pos - end_pos
    normalized_left_arrow_side = normalized_start_pos.rotate(-angle)
    normalized_right_arrow_side = normalized_start_pos.rotate(angle)
    left_arrow_pos = normalized_left_arrow_side + end_pos
    right_arrow_pos = normalized_right_arrow_side + end_pos

    pygame.draw.line(screen, color, end_pos, left_arrow_pos, width)
    pygame.draw.line(screen, color, end_pos, right_arrow_pos, width)


class Grid(Renderable):
    grid: np.ndarray
    path: np.ndarray  # matrix of 2d points to store the parent of each visited cell
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
            shape=(self.grid_width, self.grid_height, COLORS),
            dtype=np.uint8,
        )
        self.path = np.full(
            shape=(self.grid_width, self.grid_height, 2), dtype=np.int32, fill_value=-1
        )

    @staticmethod
    def default() -> "Grid":
        bounding_box = pygame.Rect(GRID_LEFT, GRID_TOP, SCREEN_WIDTH, SCREEN_WIDTH)
        return Grid(scale=GRID_SCALE, bounding_box=bounding_box)

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

    def get_cell_state(self, grid_x: int, grid_y: int) -> CellState:
        color = self.grid[grid_x, grid_y]
        state = CellState.from_color(color)
        return state

    def visit(self, parent_x: int, parent_y: int, visited_x: int, visited_y: int):
        parent_path = self.path[visited_x, visited_y]
        if parent_path[0] != -1:
            raise ValueError(
                f"Already visited cell at ({visited_x}, {visited_y}) with parent {parent_path}"
            )
        parent_path = np.array([parent_x, parent_y], dtype=np.int32)

    def render(self, screen: pygame.Surface):
        offset_x, offset_y = self.bounding_box.topleft
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                color = self.grid[x, y]
                pixel_x = x * self.scale + offset_x
                pixel_y = y * self.scale + offset_y
                rect = pygame.Rect(pixel_x, pixel_y, self.scale, self.scale)
                pygame.draw.rect(screen, color=color, rect=rect)

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                parent_pos = self.path[x, y]
                if parent_pos[0] == -1:
                    continue
                start_pos = pygame.Vector2(x, y)
                end_pos = pygame.Vector2(parent_pos)
                draw_arrow(screen, VISITED_COLOR, start_pos, end_pos)
