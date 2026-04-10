from abc import ABC, abstractmethod


class Maze(ABC):
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.maze = []
        self.forty_two = []
        self.lst_grid = []

    @abstractmethod
    def generate_maze(self) -> None:
        pass
