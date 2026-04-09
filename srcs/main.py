from algo.wilson_iterative import Maze
from visual.visual_manager import VisualManager
import data_handling.parsing as parsing
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
        self.maze.generate_maze()
        self.visual = VisualManager(3)
        entry_exit = self.get_entry_exit(self.data["ENTRY"], self.data["EXIT"])
        self.visual.get_visuals(self.maze, entry_exit)
        self.default_maze()

    def get_entry_exit(self, entry: str, exit: str) -> tuple:
        entry = entry.split(",")
        exit = exit.split(",")
        entry = (int(entry[0]), int(entry[1]))
        exit = (int(exit[0]), int(exit[1]))
        return (entry, exit)

    def default_maze(self):
        self.visual.generate_default()

    def looping(self):
        self.visual.mlx.mlx_key_hook(self.visual.window,
                                     self.visual.closing, None)
        self.visual.mlx.mlx_hook(self.visual.window, 33, 0,
                                 self.visual.gere_close, None)
        self.visual.mlx.mlx_loop(self.visual.ptr)


if __name__ == "__main__":
    handler = HandleMaze()
    handler.looping()
