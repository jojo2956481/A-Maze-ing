import sys
try:
    import mlx
    import pydantic
    mlx.Mlx()
    pydantic.AfterValidator
except ModuleNotFoundError as e:
    print("Error while importing:", e)
    sys.exit(0)
from srcs.mazegen.wilson_iterative import WilsonMaze
from srcs.mazegen.dfs_iterative import DfsMaze
from srcs.mazegen.kruskal import KruskalMaze
from srcs.visual.visual_manager import VisualManager
import srcs.data_handling.parsing as parsing
from srcs.data_handling.output_file import create_file
from enum import Enum
from typing import Any
import sys


class Commands(Enum):
    """
    enum for the command that determine the algo chosen
    """
    DFS = 65436
    KRUSKAL = 65433
    WILSON = 65435


class HandleMaze:
    """
    manager of the a_maze_ing
    """
    def __init__(self) -> None:
        """
        instantiate mazes, visualisation and a default maze
        """
        self.data = parsing.pars_dict()
        entry_exit = (tuple(self.data["ENTRY"]), tuple(self.data["EXIT"]))
        try:
            self.mazes = [DfsMaze(int(self.data["WIDTH"]),
                                  int(self.data["HEIGHT"]), entry_exit,
                                  self.data["SEED"], self.data["PERFECT"]),
                          KruskalMaze(int(self.data["WIDTH"]),
                                      int(self.data["HEIGHT"]), entry_exit,
                                      self.data["SEED"], self.data["PERFECT"]),
                          WilsonMaze(int(self.data["WIDTH"]),
                                     int(self.data["HEIGHT"]), entry_exit,
                                     self.data["SEED"], self.data["PERFECT"])]
            if self.data["HEIGHT"] < 7 or self.data["WIDTH"] < 9:
                print("The maze is too small for 42 patern.")
        except ValueError as e:
            print("[ERROR]:", e)
            sys.exit(0)
        self.actual_maze = 0
        self.mazes[self.actual_maze].generate_maze()
        window = self.data["WINDOW"] if self.data["WINDOW"] else 1
        self.visual = VisualManager(window, self.data["OUTPUT_FILE"])
        self.visual.get_visuals(self.mazes[self.actual_maze], entry_exit)
        self.default_maze()

    def default_maze(self) -> None:
        """
        generate the default window
        """
        self.visual.generate_default()

    def keyboard_management(self, keycode: int, *args: Any) -> None:
        """
        handle the algorithm change or other maze commands
        """
        if keycode not in Commands:
            self.visual.keyboard_management(keycode)
        else:
            match keycode:
                case Commands.DFS.value:
                    self.actual_maze = 0
                case Commands.KRUSKAL.value:
                    self.actual_maze = 1
                case Commands.WILSON.value:
                    self.actual_maze = 2
            self.mazes[self.actual_maze].generate_maze()
            self.visual.maze.maze = self.mazes[self.actual_maze]
            self.visual.play.maze = self.mazes[self.actual_maze]
            self.visual.path.paths = self.visual.maze.maze.paths
            self.visual.path.cell = 0
            self.visual.maze.refresh()
            create_file(self.mazes[self.actual_maze],
                        self.data["OUTPUT_FILE"])

    def looping(self) -> None:
        """
        handle the loop of the mlx
        """
        self.visual.mlx.mlx_key_hook(self.visual.window,
                                     self.keyboard_management, None)
        self.visual.mlx.mlx_hook(self.visual.window, 33, 0,
                                 self.visual.close_button, None)
        self.visual.mlx.mlx_loop(self.visual.ptr)


if __name__ == "__main__":
    handler = HandleMaze()
    handler.looping()
    handler.visual.free_mlx()
