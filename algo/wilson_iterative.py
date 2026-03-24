import random
from mlx import Mlx


class Maze:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]
        self.empty = {(i, j) for j in range(self.width)
                      for i in range(self.height)}
        self.forty_two = []
        self.get_forty_two()
        self.empty = self.empty.difference(set(self.forty_two))

    def get_forty_two(self):
        centre_i = self.height // 2
        centre_j = self.width // 2

        four = [
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]

        two = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1],
        ]

        start_i = centre_i - 2
        start_j = centre_j - 4

        for di in range(len(four)):
            for dj in range(len(four[0])):
                if four[di][dj] == 1:
                    i = start_i + di
                    j = start_j + dj
                    if 0 <= i < self.height and 0 <= j < self.width:
                        self.forty_two.append((i, j))
        for di in range(len(two)):
            for dj in range(len(two[0])):
                if two[di][dj] == 1:
                    i = start_i + di
                    j = start_j + dj + 4
                    if 0 <= i < self.height and 0 <= j < self.width:
                        self.forty_two.append((i, j))

    def generate_empty(self) -> None:
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]

    def generate_first(self) -> list:
        pos = random.choice(list(self.empty))
        end = random.choice(list(self.empty))
        visited = [pos]
        while True:
            neighboor = ["N", "E", "S", "W"]
            next = random.choice(neighboor)
            new_pos = self.get_new_pos(visited[-1], next)
            neighboor.pop(neighboor.index(next))
            while not self.check_next_good(visited, next) and neighboor:
                next = random.choice(neighboor)
                new_pos = self.get_new_pos(visited[-1], next)
                neighboor.pop(neighboor.index(next))
            if new_pos in visited:
                visited = visited[:visited.index(new_pos) + 1]
                continue
            visited.append(self.get_new_pos(visited[-1], next))
            if visited[-1] == end:
                self.empty = self.empty.difference(set(visited))
                self.open_wall(visited)
                return visited

    def generate_all_rest(self) -> list:
        pos = random.choice(list(self.empty))
        visited = [pos]
        while True:
            neighboor = ["N", "E", "S", "W"]
            next = random.choice(neighboor)
            new_pos = self.get_new_pos(visited[-1], next)
            neighboor.pop(neighboor.index(next))
            while not self.check_next_good(visited, next) and neighboor:
                next = random.choice(neighboor)
                new_pos = self.get_new_pos(visited[-1], next)
                neighboor.pop(neighboor.index(next))
            if new_pos in visited:
                visited = visited[:visited.index(new_pos) + 1]
                continue
            visited.append(self.get_new_pos(visited[-1], next))
            if visited[-1] not in self.empty:
                self.empty = self.empty.difference(set(visited))
                self.open_wall(visited)
                return visited

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

    def check_next_good(self, visited, next) -> bool:
        pos = visited[-1]
        new_pos = self.get_new_pos(pos, next)
        if (new_pos[0] >= self.height or new_pos[0] < 0 or
                new_pos[1] >= self.width or new_pos[1] < 0):
            return False
        if new_pos in self.forty_two:
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
    for cell in maze.forty_two:
        for i in range(size):
            for z in range(size):
                m.mlx_pixel_put(ptr, window, cell[1] * size + 10 + z,
                                cell[0] * size + 10 + i, 0xFFFFFFFF)


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
    maze = Maze(200, 200)
    maze.generate_empty()
    data, window, ptr, m = mlx_display(maze)
    start = time()
    maze.generate_first()
    print(f"First part: {time() - start}s")
    start = time()
    while maze.empty:
        maze.generate_all_rest()
    print(f"Second part: {time() - start}s")
    refresh(maze)
    m.mlx_key_hook(window, closing, None)
    m.mlx_hook(window, 33, 0, gere_close, None)
    m.mlx_loop(ptr)
