from abc import ABC, abstractmethod
from typing import Any


class Maze(ABC):
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.maze: list[list[dict[str, Any]]] = []
        self.forty_two: list[tuple[int, int]] = []
        self.lst_grid: list[tuple[int, int]] = []

    @abstractmethod
    def generate_maze(self) -> None:
        pass
