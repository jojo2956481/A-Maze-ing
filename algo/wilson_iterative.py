import random
from mlx import Mlx
from enum import Enum


class Coordinate(Enum):
    WEST = 8
    SOUTH = 4
    EAST = 2
    NORTH = 1


class Maze:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]
        self.empty = [(i, j) for j in range(self.width)
                      for i in range(self.height)]

    def generate_empty(self) -> None:
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]

    def generate_first(self) -> list:
        visited = []
        pos = random.choice(self.empty)
        end = random.choice(self.empty)
        visited.append([pos, 15])
        while True:
            neighboor = self.get_neighboor(visited[-1])
            if not neighboor:
                visited.pop(-1)
                continue
            next = random.choice(neighboor)
            visited[-1][1] -= next
            if (self.check_next_good(visited, next)):
                visited.append(self.get_new_pos(visited[-1], next))
                if visited[-1][0] == end:
                    visited = [cell[0] for cell in visited]
                    for cell in visited:
                        self.empty.pop(self.empty.index(cell))
                    self.open_wall(visited)
                    return visited

    def get_neighboor(self, pos):
        neighboor = []
        value = pos[-1]
        for direction in Coordinate:
            if value >= direction.value:
                value -= direction.value
                neighboor.append(direction.value)
        return neighboor

    def generate_all_rest(self) -> list:
        visited = []
        pos = random.choice(self.empty)
        visited.append([pos, 15])
        while True:
            neighboor = self.get_neighboor(visited[-1])
            if not neighboor:
                visited.pop(-1)
                continue
            next = random.choice(neighboor)
            visited[-1][1] -= next
            if (self.check_next_good(visited, next)):
                visited.append(self.get_new_pos(visited[-1], next))
                if self.is_in_maze(visited[-1][0]):
                    visited = [cell[0] for cell in visited]
                    self.open_wall(visited)
                    visited.pop(-1)
                    for cell in visited:
                        self.empty.pop(self.empty.index(cell))
                    return visited

    def get_new_pos(self, pos, next):
        pos = pos[0]
        if (next == Coordinate.NORTH.value):
            new_pos = (pos[0] - 1, pos[1])
        if (next == Coordinate.EAST.value):
            new_pos = (pos[0], pos[1] + 1)
        if (next == Coordinate.SOUTH.value):
            new_pos = (pos[0] + 1, pos[1])
        if (next == Coordinate.WEST.value):
            new_pos = (pos[0], pos[1] - 1)
        return [new_pos, 15]

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

    def check_next_good(self, visited, next) -> bool:
        pos = visited[-1]
        new_pos = self.get_new_pos(pos, next)[0]
        if (new_pos[0] >= self.height or new_pos[0] < 0 or
                new_pos[1] >= self.width or new_pos[1] < 0):
            return False
        if (new_pos in [cell[0] for cell in visited]):
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
    from time import time
    maze = Maze(20, 20)
    maze.generate_empty()
    data, window, ptr, m = mlx_display(maze)
    start = time()
    maze.generate_first()
    print(f"First part: {time() - start}s")
    start = time()
    while maze.empty != []:
        maze.generate_all_rest()
    print(f"Second part: {time() - start}s")
    refresh(maze)
    m.mlx_key_hook(window, closing, None)
    m.mlx_hook(window, 33, 0, gere_close, None)
    m.mlx_loop(ptr)
