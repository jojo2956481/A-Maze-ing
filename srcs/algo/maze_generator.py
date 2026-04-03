from abc import ABC, abstractmethod


class maze(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = []
        self.forty_two = []
        self.lst_grille = []
    

    