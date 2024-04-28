from enum import Enum
from math import floor
from typing import Optional

import numpy as np
import pygame

from search_game import gameglobals
from search_game.constants import (
    ARROW_COLOR,
    COLORS,
    END_COLOR,
    GLOW_COLOR,
    GLOW_FADE_DURATION,
    GLOW_STARTING_SIZE,
    GRID_LEFT,
    GRID_SCALE,
    GRID_TOP,
    PATH_COLOR,
    SCREEN_WIDTH,
    START_COLOR,
    VISITED_COLOR,
    WALKED_COLOR,
    WALL_COLOR,
    glow_sample_curve,
)
from search_game.renderable import Renderable

Path = list[tuple[int, int]]


class CellState(Enum):
    Wall = 0
    Path = 1
    Visited = 2
    Start = 3
    End = 4

    @staticmethod
    def from_color(color) -> "CellState":
        pygame_color = pygame.Color(color)
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
    angle: float = 15,
    width: int = 2,
    tip_length: float = 10.0,
):
    if start_pos == end_pos:
        return
    # draw the inital line
    pygame.draw.line(screen, color, start_pos, end_pos, width)

    normalized_start_pos = start_pos - end_pos
    arrow_len = normalized_start_pos.length()
    if arrow_len < 20:
        print(f"{arrow_len=}")
    normalized_start_pos = normalized_start_pos.normalize() * tip_length

    normalized_left_arrow_side = normalized_start_pos.rotate(-angle)
    normalized_right_arrow_side = normalized_start_pos.rotate(angle)
    left_arrow_pos = normalized_left_arrow_side + end_pos
    right_arrow_pos = normalized_right_arrow_side + end_pos

    pygame.draw.line(screen, color, end_pos, left_arrow_pos, width)
    pygame.draw.line(screen, color, end_pos, right_arrow_pos, width)


class Grid(Renderable):
    grid: np.ndarray
    parents: np.ndarray  # matrix of 2d points to store the parent of each visited cell
    glows: np.ndarray
    scale: int
    grid_width: int
    grid_height: int
    bounding_box: pygame.Rect
    found_path: Optional[Path]
    path_render_iter: int
    start_point: Optional[tuple[int, int]]
    end_point: Optional[tuple[int, int]]
    bfs_queue: list[tuple[int, int]]

    def __init__(self, scale: int, bounding_box: pygame.Rect):
        self.scale = scale
        self.bounding_box = bounding_box
        grid_size = pygame.Vector2(bounding_box.size) // scale
        self.grid_width = floor(grid_size.x)
        self.grid_height = floor(grid_size.y)
        self.start_point = None
        self.end_point = None
        self.path_render_iter = 0
        self.found_path = None
        self.bfs_queue = []
        self.grid = np.zeros(
            shape=(self.grid_width, self.grid_height, COLORS),
            dtype=np.uint8,
        )
        self.parents = np.full(
            shape=(self.grid_width, self.grid_height, 2), dtype=np.int32, fill_value=-1
        )
        self.glows = np.zeros(
            shape=(self.grid_width, self.grid_height), dtype=np.float32
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
        grid_pos = (grid_x, grid_y)

        if self.in_bounds(grid_pos):
            return grid_pos
        return None

    def in_bounds(self, grid_pos) -> bool:
        return (
            grid_pos[0] >= 0
            and grid_pos[0] < self.grid_width
            and grid_pos[1] >= 0
            and grid_pos[1] < self.grid_height
        )

    def grid_to_screen(self, grid_pos) -> pygame.Vector2:
        if not self.in_bounds(grid_pos):
            raise ValueError(f"Invalid grid pos: {grid_pos}")
        half_grid_scale = self.scale / 2

        x = grid_pos[0] * self.scale + self.bounding_box.left + half_grid_scale
        y = grid_pos[1] * self.scale + self.bounding_box.top + half_grid_scale

        v = pygame.Vector2(x, y)
        return v

    def place_square(self, pos: tuple[int, int], color: pygame.Color):
        if not self.in_bounds(pos):
            return
        if color == START_COLOR and self.start_point:
            self.grid[self.start_point] = PATH_COLOR

        if color == END_COLOR and self.end_point:
            self.grid[self.end_point] = PATH_COLOR

        if color != START_COLOR and self.start_point == pos:
            self.start_point = None

        if color != END_COLOR and self.end_point == pos:
            self.end_point = None

        if color == START_COLOR:
            self.start_point = pos

        if color == END_COLOR:
            self.end_point = pos

        self.grid[pos] = color
        print(f"{self.start_point=}, {self.end_point=}")

    def get_cell(self, pos: tuple[int, int]) -> CellState:
        if not self.in_bounds(pos):
            return CellState.Wall
        parent_pos = self.parents[pos]
        if parent_pos[0] != -1:
            return CellState.Visited
        grid_color = self.grid[pos]

        state = CellState.from_color(grid_color)
        return state

    def is_ready(self) -> bool:
        return self.start_point is not None and self.end_point is not None

    def init_queue(self):
        self.bfs_queue.clear()
        if not self.start_point:
            raise ValueError("Start point not set")
        self.bfs_queue.append(self.start_point)
        self.parents[self.start_point] = self.start_point
        self.glows[self.start_point] = GLOW_FADE_DURATION

    def reset_path(self):
        self.found_path = None
        self.path_render_iter = 0
        self.parents.fill(int(-1))

    def render_grid_rect(
        self,
        screen: pygame.Surface,
        pos,
        color: pygame.Color,
        scale: Optional[float] = None,
    ):
        scale = scale or self.scale
        offset_x, offset_y = self.bounding_box.topleft
        scale_offset = (scale - self.scale) // 2

        pixel_x = pos[0] * self.scale + offset_x - scale_offset
        pixel_y = pos[1] * self.scale + offset_y - scale_offset
        rect = pygame.Rect(pixel_x, pixel_y, scale, scale)
        pygame.draw.rect(screen, color=color, rect=rect)

    def grid_shape(self):
        return (self.grid_width, self.grid_height)

    def grid_indexer(self):
        return np.ndindex(self.grid_shape())

    def render_base(self, screen: pygame.Surface):
        for pos in self.grid_indexer():
            color = self.grid[pos]
            self.render_grid_rect(screen, pos, color)

    def render_visited(self, screen: pygame.Surface):
        for pos in self.grid_indexer():
            if pos in [self.start_point, self.end_point] or self.parents[pos][0] == -1:
                continue
            self.render_grid_rect(screen, pos, VISITED_COLOR)

    def render_arrows(self, screen: pygame.Surface):
        for pos in self.grid_indexer():
            parent_pos = self.parents[pos]
            if parent_pos[0] == -1:
                continue
            parent_screen_pos = self.grid_to_screen(parent_pos)
            child_screen_pos = self.grid_to_screen(pos)
            draw_arrow(screen, ARROW_COLOR, parent_screen_pos, child_screen_pos)

    def render_found_path(self, screen: pygame.Surface):
        # render found path
        if not self.found_path:
            return
        self.path_render_iter = min(self.path_render_iter + 1, len(self.found_path))
        for i in range(self.path_render_iter):
            pos = self.found_path[i]
            if pos in [self.start_point, self.end_point]:
                continue
            self.render_grid_rect(screen, pos, WALKED_COLOR)

    def render_glows(self, screen: pygame.Surface):
        for pos in self.grid_indexer():
            glow_time = self.glows[pos]
            if glow_time < 0.001:
                continue
            lerp_percent = pygame.math.clamp(glow_time / GLOW_FADE_DURATION, 0, 1)
            curved_percent = glow_sample_curve(lerp_percent)
            glow_scalar = pygame.math.lerp(
                GLOW_STARTING_SIZE, GRID_SCALE, curved_percent
            )
            self.render_grid_rect(
                screen,
                pos,
                GLOW_COLOR,
                glow_scalar,
            )

            self.glows[pos] = max(0, self.glows[pos] - gameglobals.dt)

    def render(self, screen: pygame.Surface):
        self.render_base(screen)
        self.render_glows(screen)
        self.render_visited(screen)
        self.render_found_path(screen)
        self.render_arrows(screen)
