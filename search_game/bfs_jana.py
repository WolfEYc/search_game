from typing import Optional

from search_game.constants import GLOW_FADE_DURATION
from search_game.grid import Grid, Path

# You need to implement all three functions, use trace_path and visit_grid_cell inside of bfs_jana as helper functions


def trace_path(grid: Grid, end_pos: tuple[int, int]) -> Path:
    """trace the path from the end to the start using the grid.get_parent(pos) method

    Parameters
    ----------
    parents : np.ndarray
        matrix of 2d points to store the parent of each visited cell
    end_x : int
        the x coordinate of the end point
    end_y : int
        the y coordinate of the end point

    Returns
    -------
    np.ndarray
        the path from the start to the end as a list of coordinates
    """

    path = [end_pos]

    return path


def visit_grid_cell(grid: Grid, parent_pos, visited_pos):
    """
    Visit a cell in the grid and set the parent

    Parameters
    ----------
    grid : Grid
        grid that contains state of the grid
    parent_pos : pos
        position of parent cell
    visited_pos : pos
        position of visited cell

    Raises
    ------
    ValueError
        if the cell has already been visited
    """

    grid.glows[visited_pos] = GLOW_FADE_DURATION


def bfs_jana(grid: Grid) -> Optional[Path]:
    """breadth-first search algorithm only make one step per call!

    Parameters
    ----------
    grid : Grid
        grid that contains state of the grid
        use grid.get_cell(x, y) to get the state of the cell
        use grid.visit(parent_x, parent_y, x, y) to visit a cell

    Returns
    -------
    Optional[Path]
        if a path is found on this step, return the path as a list of coordinates using trace_path
        otherwise return None (including if no step can be made)
    """

    pass
