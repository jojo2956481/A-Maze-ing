import random
from .maze import Maze


class DfsMaze(Maze):
    """
    class that inherits from class maze to
    create all methode of maze building's
    """
    def __init__(self, width: int, height: int,
                 entry_exit: tuple[tuple[int, int], tuple[int, int]],
                 seed: int | None, perfect: bool) -> None:
        """
        method to init all atributs
        """
        super().__init__(width, height, entry_exit, seed, perfect)

    def generate_maze(self) -> None:
        """
        method to manage all methods of the class
        """
        if self.seed:
            random.seed(self.seed)
        self.init_grid()
        i, j = self.start()
        self.dfs_recursive(i, j)
        if not self.perfect:
            self.imperfect_maze()

    def init_grid(self) -> None:
        """
        method to init the gride (cellule of maze)
        """
        self.lst_grid = []
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.lst_grid.append((i, j))

    def start(self) -> tuple[int, int]:
        """
        method to create the start of maze
        """
        while True:
            i, j = random.choice(self.lst_grid)
            if (i, j) not in self.forty_two:
                self.maze[i][j]["zone"] = 1
                return i, j

    def find_neighbor(self, direction: str,
                    i: int, j: int) -> tuple[int, int, str, str]:
        """
        method to find the neighbor of current cellule
        """

        ni, nj = 0, 0
        if direction == 'N':
            ni, nj = i - 1, j
            wall_cell = 'N'
            wall_neighbor = 'S'
        elif direction == 'S':
            ni, nj = i + 1, j
            wall_cell = 'S'
            wall_neighbor = 'N'
        elif direction == 'E':
            ni, nj = i, j + 1
            wall_cell = 'E'
            wall_neighbor = 'W'
        elif direction == 'W':
            ni, nj = i, j - 1
            wall_cell = 'W'
            wall_neighbor = 'E'

        return ni, nj, wall_cell, wall_neighbor

    def dfs_recursive(self, i: int, j: int) -> None:
        """
        hearth of olgo dfs: open wall using batracking
        """
        stack = [(i, j)]
        self.maze[i][j]["zone"] = 1
        while stack:
            i, j = stack[-1]

            directions = ['N', 'E', 'S', 'W']
            random.shuffle(directions)

            moved = False
            for direction in directions:
                ni, nj, wall_cell, wall_neighbor = self.find_neighbor(direction,
                                                                i, j)

                if not (0 <= ni < self.height and 0 <= nj < self.width):
                    continue
                if (ni, nj) in self.forty_two:
                    continue
                if self.maze[ni][nj]["zone"] == 0:
                    self.maze[i][j][wall_cell] = True
                    self.maze[ni][nj][wall_neighbor] = True
                    self.maze[ni][nj]["zone"] = 1

                    stack.append((ni, nj))
                    moved = True
                    break

            if not moved:
                stack.pop()
