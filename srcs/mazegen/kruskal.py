import random
from .maze import Maze


class KruskalMaze(Maze):
    """
    class that inherits from class maze to
    create all methode of maze building's
    """
    def __init__(self, width: int, height: int, entry_exit,
                 seed: int | None, perfect: bool) -> None:
        """
        method to init all atributs
        """
        super().__init__(width, height, entry_exit, perfect)
        if seed is not None:
            random.seed(seed)

    def generate_maze(self, seed: int | None = None) -> None:
        """
        method to manage all methods of the class
        """
        self.init_grid()
        self.generer(seed)

    def init_grid(self) -> None:
        """
        method to init the gride (cellule of maze)
        """
        self.maze = [[{"N": False, "E": False, "S": False, "W": False}
                      for _ in range(self.width)]
                     for _ in range(self.height)]
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.lst_grid.append((i, j))

    def generer(self, seed: int | None = None) -> None:
        """
        method to open wall
        """
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.maze[i][j]['N'] = False
                self.maze[i][j]['E'] = False
                self.maze[i][j]['S'] = False
                self.maze[i][j]['W'] = False
                zone_id += 1
        murs = []

        for i in range(self.height):
            for j in range(self.width):
                if j < self.width - 1:
                    murs.append((i, j, 'E'))
                if i < self.height - 1:
                    murs.append((i, j, 'S'))

        if seed is not None:
            random.seed(seed)
        random.shuffle(murs)
        for (i, j, direction) in murs:
            self.fusionner(i, j, direction)

    def fusionner(self, i: int, j: int, dir: str) -> bool:
        """
        method to find if zone are close
        """
        if not (0 <= i < self.height and 0 <= j < self.width):
            return False
        if (i, j) in self.forty_two:
            return False

        cellule = self.maze[i][j]
        zone1 = int(cellule['zone'])

        ni = nj = None
        mur_cell = mur_voisin = None

        if dir == 'N':
            ni, nj = i - 1, j
            mur_cell = 'N'
            mur_voisin = 'S'
        elif dir == 'S':
            ni, nj = i + 1, j
            mur_cell = 'S'
            mur_voisin = 'N'
        elif dir == 'E':
            ni, nj = i, j + 1
            mur_cell = 'E'
            mur_voisin = 'W'
        elif dir == 'W':
            ni, nj = i, j - 1
            mur_cell = 'W'
            mur_voisin = 'E'
        else:
            return False
        if not (0 <= ni < self.height and 0 <= nj < self.width):
            return False

        if (ni, nj) in self.forty_two:
            return False

        voisin = self.maze[ni][nj]
        zone2 = voisin['zone']

        if zone1 == zone2:
            return False

        cellule[mur_cell] = True
        voisin[mur_voisin] = True

        for x in range(self.height):
            for y in range(self.width):
                if self.maze[x][y]['zone'] == zone2:
                    self.maze[x][y]['zone'] = zone1
        return True
