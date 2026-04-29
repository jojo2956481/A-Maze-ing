import random
from .maze import Maze


class WilsonMaze(Maze):
    def __init__(self, width: int, height: int,
                 entry_exit: tuple[tuple[int, int], tuple[int, int]],
                 seed: int | None, perfect: bool) -> None:
        """
        instantiate parameters
        """
        super().__init__(width, height, entry_exit, seed, perfect)

    def generate_maze(self) -> None:
        """
        method to call to generate a full new maze
        """
        from time import time
        p = time()
        if self.seed:
            random.seed(self.seed)
        self.generate_empty()
        self.generate_first()
        while self.empty:
            self.generate_all_rest()
        if not self.perfect:
            self.imperfect_maze()
        self.paths = [[value[0] for value in path] for path in
                      self.solver()]
        print("Runtime: ", time() - p)

    def generate_empty(self) -> None:
        """
        method to init the gride (cellule of maze)
        """
        self.empty = {(i, j) for j in range(self.width)
                      for i in range(self.height)}
        self.empty = self.empty.difference(set(self.forty_two))
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]
        zone_id = 1
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.lst_grid.append((i, j))
        for cell in self.forty_two:
            self.maze[cell[0]][cell[1]]['zone'] = 0

    def generate_first(self) -> None:
        """
        generate the first part of the maze
        take two random cell in the maze and iterate until one found another
        """
        pos = random.choice(list(self.empty))
        end = random.choice(list(self.empty))
        while end == pos:
            end = random.choice(list(self.empty))
        visited = [pos]
        set_visited = {pos}
        directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        while True:
            neighboor = ["N", "E", "S", "W"]
            random.shuffle(neighboor)
            next = neighboor.pop()
            nx, ny = directions[next]
            new_pos = (visited[-1][0] + nx, visited[-1][1] + ny)
            while not self.check_next_good(new_pos) and neighboor:
                next = neighboor.pop()
                nx, ny = directions[next]
                new_pos = (visited[-1][0] + nx, visited[-1][1] + ny)
            if new_pos in set_visited:
                index = visited.index(new_pos) + 1
                set_visited.difference_update(set(visited[index:]))
                visited = visited[:index]
                continue
            visited.append(new_pos)
            set_visited.add(new_pos)
            if new_pos == end:
                self.empty.difference_update(set_visited)
                self.open_wall(visited)
                return

    def generate_all_rest(self) -> None:
        """
        second part of the creation
        get a random cell and iterate until it reaches a part of the maze
        """
        pos = random.choice(list(self.empty))
        visited = [pos]
        set_visited = {pos}
        directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        while True:
            neighboor = ["N", "E", "S", "W"]
            random.shuffle(neighboor)
            next = neighboor.pop()
            nx, ny = directions[next]
            new_pos = (visited[-1][0] + nx, visited[-1][1] + ny)
            while not self.check_next_good(new_pos) and neighboor:
                next = neighboor.pop()
                nx, ny = directions[next]
                new_pos = (visited[-1][0] + nx, visited[-1][1] + ny)
            if new_pos in visited:
                index = visited.index(new_pos) + 1
                set_visited.difference_update(set(visited[index:]))
                visited = visited[:index]
                continue
            visited.append(new_pos)
            set_visited.add(new_pos)
            if visited[-1] not in self.empty:
                self.empty.difference_update(set_visited)
                self.open_wall(visited)
                return

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

    def check_next_good(self, new_pos: tuple[int, int]) -> bool:
        """
        check if the next cell is valid
        """
        if (new_pos[0] >= self.height or new_pos[0] < 0 or
                new_pos[1] >= self.width or new_pos[1] < 0):
            return False
        if new_pos in self.forty_two:
            return False
        return True
