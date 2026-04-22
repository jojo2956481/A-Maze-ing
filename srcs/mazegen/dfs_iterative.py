import random
from .maze import Maze
# from srcs.transform_data.parsing import pars_dict
# from .solver import solver_bfs, solver_all_path


class DfsMaze(Maze):
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

    def generate_maze(self) -> None:
        """
        method to manage all methods of the class
        """
        self.init_grid()
        i, j = self.start()
        self.dfs_recursive(i, j)
        if not self.perfect:
            self.imperfect_maze()

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

    def start(self) -> tuple[int, int]:
        """
        method to create the start of maze
        """
        while True:
            i, j = random.choice(self.lst_grid)
            if (i, j) not in self.forty_two:
                self.maze[i][j]["zone"] = 1
                return i, j

    def find_voisin(self, direction: str,
                    i: int, j: int) -> tuple[int, int, str, str]:
        """
        method to find the voisin of current cellule
        """

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

    def solver_all_path(self) -> list[list]:
        """
        solver to find all path of maze
        """
        start = self.entry_exit[0]
        goal = self.entry_exit[1]
        all_path = []
        path = []
        path.append((start, None))
        stack = [(start, path)]

        while stack:
            current, path = stack.pop()
            i, j = current
            if current == goal:
                all_path.append(path.copy())
                continue
            cell = self.maze[i][j]
            directions = [
                ('N', (-1, 0)),
                ('S', (1, 0)),
                ('E', (0, 1)),
                ('W', (0, -1))
            ]
            for direction, (di, dj) in directions:
                if cell[direction]:
                    ni, nj = i + di, j + dj
                    neighbor = (ni, nj)
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        if neighbor not in [p[0] for p in path]:
                            stack.append(
                                (neighbor, path +
                                 [(neighbor, direction)]))
        # print(len(sorted(all_path, key=lambda x: len(x))))
        return sorted(all_path, key=lambda x: len(x))

    def imperfect_maze(self) -> None:
        """
        broke wall to make maze imperfect
        """
        directions = {
            'N': (-1, 0, 'S'),
            'S': (1, 0, 'N'),
            'E': (0, 1, 'W'),
            'W': (0, -1, 'E')
        }
        count = 1
        while (count < 3):
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
            dir_name = random.choice(list(directions.keys()))
            di, dj, opposite = directions[dir_name]
            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if not self.maze[i][j][dir_name]:
                    if self.maze[i][j]["zone"] != 0:
                        if self.maze[ni][nj]["zone"] != 0:

                            self.maze[i][j][dir_name] = True
                            self.maze[ni][nj][opposite] = True
                            solution = self.solver_all_path()
                            if len(solution) <= count:
                                self.maze[i][j][dir_name] = False
                                self.maze[ni][nj][opposite] = False
                            else:
                                count += 1
