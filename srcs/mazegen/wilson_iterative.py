import random
from .maze import Maze


class WilsonMaze(Maze):
    def __init__(self, width: int, height: int,
                 entry_exit: tuple[tuple[int, int], tuple[int, int]],
                 seed: int | None, perfect: bool) -> None:
        """
        instantiate parameters
        """
        super().__init__(width, height, entry_exit, perfect)
        if seed is not None:
            random.seed(seed)

    def generate_maze(self) -> None:
        """
        method to call to generate a full new maze
        """
        self.generate_empty()
        self.empty = {(i, j) for j in range(self.width)
                      for i in range(self.height)}
        self.empty = self.empty.difference(set(self.forty_two))
        self.generate_first()
        while self.empty:
            self.generate_all_rest()

    def generate_empty(self) -> None:
        """
        generate empty maze
        """
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]

    def generate_first(self) -> None:
        """
        generate the first part of the maze
        take two random cell in the maze and iterate until one found another
        """
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
                return

    def generate_all_rest(self) -> None:
        """
        second part of the creation
        get a random cell and iterate until it reaches a part of the maze
        """
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
                return

    def get_new_pos(self, pos: tuple[int, int], next: str) -> tuple[int, int]:
        """
        get the new cell positions depending of the direction
        """
        if (next == "N"):
            new_pos = (pos[0] - 1, pos[1])
        if (next == "E"):
            new_pos = (pos[0], pos[1] + 1)
        if (next == "S"):
            new_pos = (pos[0] + 1, pos[1])
        if (next == "W"):
            new_pos = (pos[0], pos[1] - 1)
        return new_pos

    def open_wall(self, visited: list[tuple[int, int]]) -> None:
        """
        open the walls between two cells with the list of visited cells
        """
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

    def open_neighnbor(self, cell: tuple[int, int], direction: str) -> None:
        """
        open two cells determined with a cell and the cell in the direction
        """
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

    def check_next_good(self, visited: list[tuple[int, int]],
                        next: str) -> bool:
        """
        check if the next cell is valid
        """
        pos = visited[-1]
        new_pos = self.get_new_pos(pos, next)
        if (new_pos[0] >= self.height or new_pos[0] < 0 or
                new_pos[1] >= self.width or new_pos[1] < 0):
            return False
        if new_pos in self.forty_two:
            return False
        return True
