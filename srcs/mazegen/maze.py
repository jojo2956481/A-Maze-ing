from abc import ABC, abstractmethod
from typing import Any
import random


class Maze(ABC):
    def __init__(
            self, width: int, height: int,
            entry_exit: tuple[tuple[int, int], tuple[int, int]],
            seed: int | None, perfect: bool) -> None:
        """
        instantiate attribut of the maze
        """
        self.width: int = width
        self.height: int = height
        self.entry, self.exit = entry_exit
        self.maze: list[list[dict[str, Any]]] = []
        self.forty_two: list[tuple[int, int]] = []
        if self.width >= 9 and self.height >= 7:
            self.place_42()
        self.lst_grid: list[tuple[int, int]] = []
        self.perfect = perfect
        self.seed = seed
        self.generate_maze()

    @abstractmethod
    def generate_maze(self) -> None:
        pass

    def place_42(self) -> None:
        """
        place the pattern 42 on the grid
        """
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
        if self.entry[::-1] in self.forty_two:
            raise ValueError("Entry can't be placed in the 42")
        if self.exit[::-1] in self.forty_two:
            raise ValueError("Exit can't be placed in the 42")

    def solver(self) -> list[list[tuple[tuple[int, int], Any]]]:
        """
        A solver that found every path possible of the maze
        """
        start, exit = self.entry, self.exit
        visited = {start}
        paths = []
        directions = [
                ("N", (0, -1)), ("E", (1, 0)),
                ("S", (0, 1)), ("W", (-1, 0))
            ]
        actual_path: list[tuple[
            tuple[int, int], Any, Any]] = [(start, None, directions.copy())]
        while actual_path:
            if not actual_path[-1][2]:
                pos, _, _ = actual_path.pop()
                visited.remove(pos)
                continue
            current, _, neighbors = actual_path[-1]
            if current == exit:
                path = [cell[0:2] for cell in actual_path]
                paths.append(path.copy())
                if self.perfect:
                    return paths
                pos, _, _ = actual_path.pop()
                visited.remove(pos)
                continue
            direction = random.choice(neighbors)
            actual_path[-1][2].remove(direction)
            cell = self.maze[current[1]][current[0]]
            new_pos = (current[0] + direction[1][0],
                       current[1] + direction[1][1])
            if self.check_next_pos(new_pos, direction,
                                   visited, cell):
                actual_path.append((new_pos, direction[0], directions.copy()))
                visited.add(new_pos)
        return paths

    def check_next_pos(self, new_pos: tuple[int, int],
                       direction: tuple[str, tuple[int, int]],
                       visited: set[tuple[int, int]],
                       cell: dict[str, bool]) -> bool:
        """
        check if the given pos is valid
        """
        if (new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= self.width
                or new_pos[1] >= self.height):
            return False
        if not cell[direction[0]]:
            return False
        if new_pos in visited:
            return False
        return True

    def imperfect_maze(self) -> None:
        """
        broke wall to make maze imperfect
        """
        if self.width < 5 or self.height < 5:
            return
        directions = {
            'N': (0, -1, 'S'),
            'S': (0, 1, 'N'),
            'E': (1, 0, 'W'),
            'W': (-1, 0, 'E')
        }
        count = 1
        while (count < 3):
            temp = [cell[0] for cell in self.solver()[0]]
            (i, j) = random.choice(temp)
            dir_name = random.choice(list(directions.keys()))
            di, dj, opposite = directions[dir_name]
            ni, nj = i + di, j + dj
            if 0 <= nj < self.height and 0 <= ni < self.width:
                if not self.maze[j][i][dir_name]:
                    if self.maze[j][i]["zone"] != 0:
                        if self.maze[nj][ni]["zone"] != 0:

                            self.maze[j][i][dir_name] = True
                            self.maze[nj][ni][opposite] = True
                            solution = self.solver()
                            if len(solution) <= count:
                                self.maze[j][i][dir_name] = False
                                self.maze[nj][ni][opposite] = False
                            else:
                                count += 1
