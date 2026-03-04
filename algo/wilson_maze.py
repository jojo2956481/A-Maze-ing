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
                       end: tuple = None, visited=[],
                       gen: Generator = None) -> Generator:
        if pos is None:
            visited = []
            gen = self.count()
            pos = random.choice(self.empty)
            end = random.choice(self.empty)
        count = next(gen)
        if count > 1000:
            yield "Not found"
        visited.append(pos)
        neighboor = ["N", "E", "S", "W"]
        while neighboor != []:
            nexte = random.choice(neighboor)
            neighboor.pop(neighboor.index(nexte))
            if (self.check_next_good(pos, visited, nexte)):
                new_pos = self.get_new_pos(pos, nexte)
                if new_pos == end:
                    visited.append(new_pos)
                    for cell in visited:
                        self.empty.pop(self.empty.index(cell))
                    self.open_wall(visited)
                    yield "Finished"
                yield from self.generate_first(new_pos, end, visited, gen)
                visited.pop(visited.index(new_pos))

    def count(self) -> Generator:
        count = 0
        while True:
            count += 1
            yield count

    def generate_all_rest(self, pos: tuple = None, visited=[],
                          gen: Generator = None) -> Generator:
        if pos is None:
            if self.empty == []:
                yield "Finished"
            visited = []
            gen = self.count()
            pos = random.choice(self.empty)
        visited.append(pos)
        count = next(gen)
        neighboor = ["N", "E", "S", "W"]
        if count > 1000:
            yield "Not found"
        while neighboor != []:
            nexte = random.choice(neighboor)
            neighboor.pop(neighboor.index(nexte))
            if (self.check_next_good(pos, visited, nexte)):
                new_pos = self.get_new_pos(pos, nexte)
                if self.is_in_maze(new_pos):
                    visited.append(new_pos)
                    self.open_wall(visited)
                    visited.pop(-1)
                    for cell in visited:
                        self.empty.pop(self.empty.index(cell))
                    yield "Continuing"
                yield from self.generate_all_rest(new_pos, visited, gen)
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

    def open_wall(self, visited) -> None:
        for i in range(len(visited) - 1):
            if visited[i][0] - visited[i + 1][0] == 1:
                direction = "N"
            elif visited[i][1] - visited[i + 1][1] == -1:
                direction = "E"
            elif visited[i][0] - visited[i + 1][0] == -1:
                direction = "S"
            else:
                direction = "W"
            self.open_neighnbor(visited[i], direction)

    def open_neighnbor(self, cell: tuple, direction: str) -> None:
        if direction == "N":
            self.maze[cell[0]][cell[1]]["N"] = True
            self.maze[cell[0] - 1][cell[1]]["S"] = True
        elif direction == "E":
            self.maze[cell[0]][cell[1]]["E"] = True
            self.maze[cell[0]][cell[1] + 1]["W"] = True
        elif direction == "S":
            self.maze[cell[0]][cell[1]]["S"] = True
            self.maze[cell[0] + 1][cell[1]]["N"] = True
        else:
            self.maze[cell[0]][cell[1]]["W"] = True
            self.maze[cell[0]][cell[1] - 1]["E"] = True

    def check_next_good(self, pos, visited, next) -> bool:
        new_pos = self.get_new_pos(pos, next)
        if (new_pos[0] >= self.height or new_pos[0] < 0 or
                new_pos[1] >= self.width or new_pos[1] < 0):
            return False
        if (new_pos in visited):
            return False
        return True

    def is_in_maze(self, pos) -> bool:
        if pos not in self.empty:
            return True
        return False


def refresh(maze: Maze):
    m.mlx_clear_window(ptr, window)
    size = int(((data[1] / 2) / maze.width - 1) / 2)
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


def mlx_display(maze: Maze) -> None:
    m = Mlx()
    ptr = m.mlx_init()
    data = m.mlx_get_screen_size(ptr)
    size = int(((data[1] / 2) / maze.width - 1) / 2)
    window = m.mlx_new_window(ptr, int(size * maze.width + 20),
                              int(size * maze.height + 20), "Maze")
    return data, window, ptr, m


def gere_close(dummy):
    m.mlx_loop_exit(ptr)


def closing(keycode, params):
    if keycode == 113:
        m.mlx_loop_exit(ptr)


if __name__ == "__main__":
    maze = Maze(20, 20)
    maze.generate_empty()
    data, window, ptr, m = mlx_display(maze)
    gen = maze.generate_first()
    temp = next(gen)
    while (temp != "Finished"):
        gen = maze.generate_first()
    gen = maze.generate_all_rest()
    temp = next(gen)
    while temp != "Finished":
        gen = maze.generate_all_rest()
        temp = next(gen)
    refresh(maze)
    m.mlx_key_hook(window, closing, None)
    m.mlx_hook(window, 33, 0, gere_close, None)
    m.mlx_loop(ptr)
