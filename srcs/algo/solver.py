from collections import deque
from typing import Any
from .maze import Maze


def solver_bfs(entry, exit, maze: Any) -> str:
    e_x, e_y = map(int, entry.split(","))
    o_x, o_y = map(int, exit.split(","))

    start = (e_y, e_x)
    goal = (o_y, o_x)

    queue = deque([start])
    visited = set()
    parents = {}

    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            break
        i, j = current
        cell = maze.maze[i][j]
        directions = [
            ('N', (-1, 0)),
            ('S', (1, 0)),
            ('E', (0, 1)),
            ('W', (0, -1))
        ]
        for direction, (di, dj) in directions:
            if cell[direction]:
                ni, nj = i + di, j + dj
                neighbor = (ni, nj)
                if 0 <= ni < maze.height and 0 <= nj < maze.width:
                    neighbor = (ni, nj)
                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = (current, direction)
                    queue.append(neighbor)
    path = []
    lst = ""
    current = goal
    while current != start:
        parent, direction = parents[current]
        path.append((current, direction))
        current = parent
    path.append((start, None))
    path.reverse()
    for cell, direction in path:
        if direction is not None:
            lst += direction
    return path


def solver_all_path(entry_exit: tuple[tuple[int, int], tuple[int, int]],
                    maze: Maze) -> list[list]:
    start = entry_exit[0]
    goal = entry_exit[1]
    all_path = []
    path = []
    path.append((start, None))
    stack = [(start, path)]

    while stack:
        current, path = stack.pop()
        i, j = current
        if current == goal:
            all_path.append(path.copy())
            continue
        cell = maze.maze[i][j]
        directions = [
            ('N', (-1, 0)),
            ('S', (1, 0)),
            ('E', (0, 1)),
            ('W', (0, -1))
        ]
        for direction, (di, dj) in directions:
            if cell[direction]:
                ni, nj = i + di, j + dj
                neighbor = (ni, nj)
                if 0 <= ni < maze.height and 0 <= nj < maze.width:
                    if neighbor not in [p[0] for p in path]:
                        stack.append((neighbor, path +
                                      [(neighbor, direction)]))
    return sorted(all_path, key=lambda x: len(x))
