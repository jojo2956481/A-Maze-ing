import random


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.forty_two = []
        self.get_forty_two()

    def generate_maze(self) -> None:
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]
        self.empty = {(i, j) for j in range(self.width)
                      for i in range(self.height)}
        self.empty = self.empty.difference(set(self.forty_two))
        self.generate_first()
        while self.empty:
            self.generate_all_rest()

    def get_forty_two(self) -> None:
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
