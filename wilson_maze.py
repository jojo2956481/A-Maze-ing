import random
from typing import Generator
from mlx import Mlx


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = []
        self.empty = [(i, j) for j in range(self.width)
                      for i in range(self.height)]

    def generate_empty(self) -> None:
        for line in range(self.height):
            line = []
            for cell in range(self.width):
                line.append({"N": False, "E": False, "S": False, "W": False})
            self.maze.append(line)

    def generate_first(self, pos: tuple = None,
                       end: tuple = None, visited=[]) -> Generator:
        if pos is None:
            pos = random.choice(self.empty)
            end = random.choice(self.empty)
        visited.append(pos)
        neighboor = ["N", "E", "S", "W"]
        while neighboor != []:
            next = random.choice(neighboor)
            neighboor.pop(neighboor.index(next))
            if (self.check_next_good(pos, visited, next)):
                new_pos = self.get_new_pos(pos, next)
                self.open_wall(pos, new_pos, next)
                if new_pos == end:
                    visited.append(new_pos)
                    for cell in visited:
                        self.empty.pop(self.empty.index(cell))
                    yield "Finished"
                yield from self.generate_first(new_pos, end, visited)
                self.close_wall(pos, new_pos, next)
                visited.pop(visited.index(new_pos))

    def generate_all_rest(self, pos: tuple = None, visited=[]) -> Generator:
        if pos is None:
            if self.empty == []:
                yield "Finished"
            visited = []
            pos = random.choice(self.empty)
            visited.append(pos)
        neighboor = ["N", "E", "S", "W"]
        while neighboor != []:
            next = random.choice(neighboor)
            neighboor.pop(neighboor.index(next))
            if (self.check_next_good(pos, visited, next)):
                new_pos = self.get_new_pos(pos, next)
                if self.is_in_maze(new_pos):
                    self.open_wall(pos, new_pos, next)
                    for cell in visited:
                        self.empty.pop(self.empty.index(cell))
                    yield "Continuing"
                visited.append(new_pos)
                self.open_wall(pos, new_pos, next)
                yield from self.generate_all_rest(new_pos, visited)
                self.close_wall(pos, new_pos, next)
                visited.pop(visited.index(new_pos))
        if self.empty == []:
            yield "Finished"

    def get_new_pos(self, pos, next):
        if (next == "N"):
            new_pos = (pos[0] - 1, pos[1])
        if (next == "E"):
            new_pos = (pos[0], pos[1] + 1)
        if (next == "S"):
            new_pos = (pos[0] + 1, pos[1])
        if (next == "W"):
            new_pos = (pos[0], pos[1] - 1)
        return new_pos

    def open_wall(self, pos, new_pos, next) -> None:
        neighboor = ["N", "E", "S", "W"]
        prev = (neighboor.index(next) + 2) % 4
        self.maze[pos[0]][pos[1]][next] = True
        self.maze[new_pos[0]][new_pos[1]][neighboor[prev]] = True

    def close_wall(self, pos, new_pos, next):
        neighboor = ["N", "E", "S", "W"]
        prev = (neighboor.index(next) + 2) % 4
        self.maze[pos[0]][pos[1]][next] = False
        self.maze[new_pos[0]][new_pos[1]][neighboor[prev]] = False

    def check_next_good(self, pos, visited, next) -> bool:
        new_pos = self.get_new_pos(pos, next)
        if (new_pos[0] >= self.height or new_pos[0] < 0 or
                new_pos[1] >= self.width or new_pos[1] < 0):
            return False
        if (new_pos in visited):
            return False
        return True

    def is_in_maze(self, pos) -> bool:
        walls = self.maze[pos[0]][pos[1]]
        for wall in walls.values():
            if wall:
                return True
        return False


def mlx_display(maze: Maze) -> None:
    m = Mlx()
    ptr = m.mlx_init()
    data = m.mlx_get_screen_size(ptr)
    size = int(((data[1] / 2) / maze.width - 1) / 2)
    window = m.mlx_new_window(ptr, int(size * maze.width + 20),
                              int(size * maze.height + 20), "Maze")
    i = 10
    j = 10
    for line in maze.maze:
        for cell in line:
            if not cell["N"]:
                for n in range(size):
                    m.mlx_pixel_put(ptr, window, i + n, j, 0xFFFFFFFF)
            if not cell["E"]:
                for n in range(size):
                    m.mlx_pixel_put(ptr, window, i + size - 1,
                                    j + n, 0xFFFFFFFF)
            if not cell["S"]:
                for n in range(size):
                    m.mlx_pixel_put(ptr, window, i + n,
                                    j + size - 1, 0xFFFFFFFF)
            if not cell["W"]:
                for n in range(size):
                    m.mlx_pixel_put(ptr, window, i, j + n, 0xFFFFFFFF)
            i += size
        i = 10
        j += size

    def gere_close(dummy):
        m.mlx_loop_exit(ptr)

    m.mlx_mouse_hook(window, None, None)
    m.mlx_hook(window, 33, 0, gere_close, None)
    m.mlx_loop(ptr)


if __name__ == "__main__":
    maze = Maze(20, 15)
    maze.generate_empty()
    gen = maze.generate_first()
    next(gen)
    gen = maze.generate_all_rest()
    temp = next(gen)
    while temp != "Finished":
        gen = maze.generate_all_rest()
        temp = next(gen)
    mlx_display(maze)
