from typing import Optional

from search_game.grid import Grid, Path


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


def bfs(grid: Grid) -> Optional[Path]:
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
