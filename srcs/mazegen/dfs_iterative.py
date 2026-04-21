import random
from typing import Any
# from solver import solver_all_path
# from srcs.transform_data.parsing import pars_dict
# from .solver import solver_bfs, solver_all_path


class DfsMaze():
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.maze: list[list[dict[str, Any]]] = []
        self.forty_two: list[tuple[int, int]] = []
        self.lst_grille: list[tuple[int, int]] = []
        for i in range(height):
            ligne: list[dict[str, Any]] = []
            for j in range(width):
                cellule = {'N': False, 'E': False, 'S': False,
                           'W': False, 'zone': 1}
                ligne.append(cellule)
            self.maze.append(ligne)

    def generate_maze(self, seed: int | None = None) -> None:
        self.init_grille()
        self.place_42()
        if seed is not None:
            random.seed(seed)
        i, j = self.start()
        self.dfs_recursive(i, j)

    def execute_dfs(self, seed: int | None = None) -> None:
        if seed is not None:
            random.seed(seed)
        i, j = self.start()
        self.dfs_recursive(i, j)

    def init_grille(self) -> None:
        zone_id = 0
        for i in range(self.height):
            for j in range(self.width):
                self.maze[i][j]['zone'] = zone_id
                self.maze[i][j]['N'] = False
                self.maze[i][j]['E'] = False
                self.maze[i][j]['S'] = False
                self.maze[i][j]['W'] = False
                self.lst_grille.append((i, j))

    def start(self) -> tuple[int, int]:
        while True:
            i, j = random.choice(self.lst_grille)
            if (i, j) not in self.forty_two:
                self.maze[i][j]["zone"] = 1
                return i, j

    def find_voisin(self, direction: str,
                    i: int, j: int) -> tuple[int, int, str, str]:

        ni, nj = 0, 0
        if direction == 'N':
            ni, nj = i - 1, j
            mur_cell = 'N'
            mur_voisin = 'S'
        elif direction == 'S':
            ni, nj = i + 1, j
            mur_cell = 'S'
            mur_voisin = 'N'
        elif direction == 'E':
            ni, nj = i, j + 1
            mur_cell = 'E'
            mur_voisin = 'W'
        elif direction == 'W':
            ni, nj = i, j - 1
            mur_cell = 'W'
            mur_voisin = 'E'

        return ni, nj, mur_cell, mur_voisin

    def dfs_recursive(self, i: int, j: int) -> None:
        stack = [(i, j)]
        self.maze[i][j]["zone"] = 1
        while stack:
            i, j = stack[-1]

            directions = ['N', 'E', 'S', 'W']
            random.shuffle(directions)

            moved = False
            for direction in directions:
                ni, nj, mur_cell, mur_voisin = self.find_voisin(direction,
                                                                i, j)

                if not (0 <= ni < self.height and 0 <= nj < self.width):
                    continue
                if (ni, nj) in self.forty_two:
                    continue
                if self.maze[ni][nj]["zone"] == 0:
                    self.maze[i][j][mur_cell] = True
                    self.maze[ni][nj][mur_voisin] = True
                    self.maze[ni][nj]["zone"] = 1

                    stack.append((ni, nj))
                    moved = True
                    break

            if not moved:
                stack.pop()

    def place_42(self) -> None:
        centre_i = self.height // 2
        centre_j = (
            self.width // 2 + 1 if self.width % 2 == 1 else self.width // 2)

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

    def imperfect_maze(self) -> None:
        mur = 0
        for ligne in self.maze:
            for cell in ligne:
                for value in cell.values():
                    if value is False:
                        mur += 1
        mur = mur // 2
        mur = mur - (self.height + self.width)
        mur = mur - 55
        # result = int(mur * 0.5)
        directions = {
            'N': (-1, 0, 'S'),
            'S': (1, 0, 'N'),
            'E': (0, 1, 'W'),
            'W': (0, -1, 'E')
        }
        count = 0
        while (count < 0):
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)

            dir_name = random.choice(list(directions.keys()))
            di, dj, opposite = directions[dir_name]

            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if not self.maze[i][j][dir_name]:
                    if self.maze[i][j]["zone"] != 0:
                        if self.maze[ni][nj]["zone"] != 0:
                            if sum(1 for v in self.maze[i][j].values()
                                   if not v) >= 1:
                                if sum(1 for v in self.maze[ni][nj].values()
                                       if not v) >= 1:

                                    self.maze[i][j][dir_name] = True
                                    self.maze[ni][nj][opposite] = True
