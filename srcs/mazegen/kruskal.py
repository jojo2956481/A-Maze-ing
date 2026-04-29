import random
from .maze import Maze


class KruskalMaze(Maze):
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
        self.zone_dict: dict[str, list[tuple[int, int]]] = {}

    def generate_maze(self) -> None:
        """
        method to manage all methods of the class
        """
        if self.seed:
            random.seed(self.seed)
        self.init_grid()
        self.generate()
        if not self.perfect:
            self.imperfect_maze()

    def init_grid(self) -> None:
        """
        method to init the gride (cell of maze)
        """
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]
        zone_id = 1
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.lst_grid.append((i, j))
                zone_id += 1
        for cell in self.forty_two:
            self.maze[cell[1]][cell[0]]['zone'] = 0

    def generate(self) -> None:
        """
        method to open wall
        """
        zone_id = 1
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.maze[i][j]['N'] = False
                self.maze[i][j]['E'] = False
                self.maze[i][j]['S'] = False
                self.maze[i][j]['W'] = False
                self.zone_dict[str(zone_id)] = [(i, j)]
                zone_id += 1
        walls = []

        for i in range(self.height):
            for j in range(self.width):
                if j < self.width - 1:
                    walls.append((i, j, 'E'))
                if i < self.height - 1:
                    walls.append((i, j, 'S'))

        random.shuffle(walls)
        for (i, j, direction) in walls:
            self.merge(i, j, direction)

    def merge(self, i: int, j: int, dir: str) -> bool:
        """
        method to find if zone are close
        """
        if not (0 <= i < self.height and 0 <= j < self.width):
            return False
        if (i, j) in self.forty_two:
            return False

        cell = self.maze[i][j]
        zone1 = int(cell['zone'])

        ni = nj = None
        wall_cell = wall_neighbor = None

        if dir == 'N':
            ni, nj = i - 1, j
            wall_cell = 'N'
            wall_neighbor = 'S'
        elif dir == 'S':
            ni, nj = i + 1, j
            wall_cell = 'S'
            wall_neighbor = 'N'
        elif dir == 'E':
            ni, nj = i, j + 1
            wall_cell = 'E'
            wall_neighbor = 'W'
        elif dir == 'W':
            ni, nj = i, j - 1
            wall_cell = 'W'
            wall_neighbor = 'E'
        else:
            return False
        if not (0 <= ni < self.height and 0 <= nj < self.width):
            return False

        if (ni, nj) in self.forty_two:
            return False

        neighbor = self.maze[ni][nj]
        zone2 = neighbor['zone']

        if zone1 == zone2:
            return False

        cell[wall_cell] = True
        neighbor[wall_neighbor] = True

        for pos in self.zone_dict[str(zone2)]:
            self.maze[pos[0]][pos[1]]['zone'] = zone1
        self.zone_dict[str(zone1)] += self.zone_dict[str(zone2)]
        return True
