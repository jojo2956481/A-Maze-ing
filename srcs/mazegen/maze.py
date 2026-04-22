from abc import ABC, abstractmethod
from typing import Any


class Maze(ABC):
    def __init__(
            self, width: int, height: int,
            entry_exit: tuple[tuple[int, int], tuple[int, int]],
            perfect: bool) -> None:
        self.width: int = width
        self.height: int = height
        self.entry, self.exit = entry_exit
        self.maze: list[list[dict[str, Any]]] = []
        self.forty_two: list[tuple[int, int]] = []
        self.place_42()
        self.lst_grid: list[tuple[int, int]] = []
        self.perfect = perfect

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
