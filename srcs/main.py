from algo.wilson_iterative import Maze
from parsing.visual import Visual
import parsing.parsing as parsing
from enum import Enum
# from algo.genere_maze import Maze


class Commands(Enum):
    QUIT = 113
    NEXT_COLOR = 99
    NEW_MAZE = 110
    RANDOM_COLOR = 114


class HandleMaze:
    def __init__(self):
        self.data = parsing.pars_dict()
        self.maze = Maze(int(self.data["WIDTH"]), int(self.data["HEIGHT"]))
        self.visual = Visual(self.maze)
        self.default_maze()

    def default_maze(self):
        self.maze.generate_maze()
        self.visual.create_window()
        self.visual.create_maze_image()
        self.visual.refresh()

    def looping(self):
        self.visual.mlx.mlx_key_hook(self.visual.window,
                                     self.visual.closing, None)
        self.visual.mlx.mlx_hook(self.visual.window, 33, 0,
                                 self.visual.gere_close, None)
        self.visual.mlx.mlx_loop(self.visual.ptr)


if __name__ == "__main__":
    handler = HandleMaze()
    handler.looping()
