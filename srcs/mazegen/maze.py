from abc import ABC, abstractmethod


class Maze(ABC):
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.maze: list = []
        self.forty_two: list = []
        self.lst_grid: list = []

    @abstractmethod
    def generate_maze(self) -> None:
        pass
