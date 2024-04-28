from typing import Optional

from search_game.constants import GLOW_FADE_DURATION
from search_game.grid import CellState, Grid, Path


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
    Path
        the path from the start to the end as a list of positions
    """

    path = [end_pos]
    while path[-1] != grid.start_point:
        print("tracing_path:", path[-1])
        parent_pos = grid.parents[path[-1]]
        parent_pos = tuple(parent_pos)
        path.append(parent_pos)
    return path


def visit_grid_cell(grid: Grid, parent_pos, visited_pos):
    """Visit a cell in the grid and set the parent

    Parameters
    ----------
    grid : Grid
        grid that contains state of the grid
    parent_pos : _type_
        position of parent cell
    visited_pos : _type_
        position of visited cell

    Raises
    ------
    ValueError
        if the cell has already been visited
    """

    parent_path = grid.parents[visited_pos]
    if parent_path[0] != -1:
        raise ValueError(
            f"Already visited cell at {visited_pos} with parent {parent_path}"
        )
    grid.parents[visited_pos] = parent_pos
    grid.glows[visited_pos] = GLOW_FADE_DURATION


def bfs_isaac(grid: Grid) -> Optional[Path]:
    """breadth-first search algorithm only make one step per call!

    Parameters
    ----------
    grid : Grid
        grid that contains state of the grid
        use grid.get_cell(x, y) to get the state of the cell
        use grid.visit(parent_x, parent_y, x, y) to visit a cell
        use grid.bfs_queue as the queue for the bfs algorithm

    Returns
    -------
    Optional[Path]
        if a path is found on this step, return the path as a list of coordinates using trace_path
        otherwise return None (including if no step can be made)
    """
    if len(grid.bfs_queue) == 0:
        return None

    parent_pos = grid.bfs_queue.pop(0)
    left_neighbor = (parent_pos[0] - 1, parent_pos[1])
    right_neighbor = (parent_pos[0] + 1, parent_pos[1])
    up_neighbor = (parent_pos[0], parent_pos[1] - 1)
    down_neighbor = (parent_pos[0], parent_pos[1] + 1)
    neighbors = [left_neighbor, right_neighbor, up_neighbor, down_neighbor]

    valid_neighbors = filter(
        lambda x: grid.get_cell(x) in [CellState.Path, CellState.End], neighbors
    )

    for neighbor in valid_neighbors:
        visit_grid_cell(grid, parent_pos, neighbor)
        if neighbor == grid.end_point:
            return trace_path(grid, neighbor)
        grid.bfs_queue.append(neighbor)

    return None
