import random
from .maze import Maze
# # from collections import deque
# from srcs.transform_data.parsing import pars_dict


class KruskalMaze(Maze):
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.maze = []
        self.forty_two = []
        self.lst_grid = []
        for i in range(height):
            ligne = []
            for j in range(width):
                cellule = {'N': False, 'E': False, 'S': False,
                           'W': False, 'zone': 1}
                ligne.append(cellule)
            self.maze.append(ligne)

    def generate_maze(self) -> None:
        self.place_42()
        self.init_grille()
        self.generer()

    def init_grille(self) -> None:
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.maze[i][j]['N'] = False
                self.maze[i][j]['E'] = False
                self.maze[i][j]['S'] = False
                self.maze[i][j]['W'] = False
                self.lst_grid.append((i, j))

    def generer(self, seed: int | None = None) -> None:
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

    def place_42(self) -> None:
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
