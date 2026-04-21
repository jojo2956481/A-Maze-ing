from collections import deque
from typing import Any
from .maze import Maze
from enum import Enum


def solver_bfs(entry_exit: tuple[tuple[int, int], tuple[int, int]],
                    maze: Maze) -> list:

    import time
    p = time.time()

    start = entry_exit[0]
    goal = entry_exit[1]

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
    print(time.time() - p)
    return [path]


def solver_all_path(entry_exit: tuple[tuple[int, int], tuple[int, int]],
                    maze: Maze) -> list[list]:
    # import time
    # p = time.time()
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
    # print(time.time() - p)
    return sorted(all_path, key=lambda x: len(x))


def solver_test(entry_exit: tuple[tuple[int, int],
                                  tuple[int, int]], maze: Maze) -> list[int]:
    from time import time
    banned = set()
    paths = []
    directions = [
            ("N", (0, -1)), ("E", (1, 0)),
            ("S", (0, 1)), ("W", (-1, 0))
        ]
    actual_path = [[(entry_exit[0]), None, directions]]
    exit = entry_exit[1]
    p = time()
    while actual_path:
        print(actual_path)
        while not actual_path[0][2]:
            cell, _, _ = actual_path.pop()
        current, _, neighbors = actual_path[-1]
        if current == exit:
            path = [cell[0:2] for cell in actual_path]
            paths.append(path.copy())
            continue
        count = 0
        for direction in neighbors:
            new_pos = (current[0] + direction[1][0],
                       current[1] + direction[1][1])
            if check_next_good(new_pos, direction, actual_path,
                               maze, banned):
                neighbor = current + direction[1]
                actual_path.append((neighbor, direction[0], directions))
                count += 1
        if count == 0:
            banned = banned.union(current)
    print(paths)
    print("Runtime:", time() - p)
    return paths


def check_next_good(new_pos, direction, actual_path, maze, banned):
    cell = maze.maze[new_pos[0]][new_pos[1]]
    if not cell[direction[0]]:
        return False
    if tuple(new_pos) in banned:
        return False
    if new_pos in actual_path:
        return False
    return True
