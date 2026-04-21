import sys
try:
    import mlx
    mlx.Mlx()
except ModuleNotFoundError as e:
    print("Error while importing:", e)
    sys.exit(0)
from srcs.mazegen.wilson_iterative import WilsonMaze
from srcs.mazegen.dfs_iterative import DfsMaze
from srcs.mazegen.kruskal import KruskalMaze
from srcs.visual.visual_manager import VisualManager
import srcs.data_handling.parsing as parsing
from enum import Enum
from typing import Any


class Commands(Enum):
    DFS = 65436
    KRUSKAL = 65433
    WILSON = 65435


class HandleMaze:
    def __init__(self) -> None:
        self.data = parsing.pars_dict()
        self.mazes = [DfsMaze(int(self.data["WIDTH"]),
                              int(self.data["HEIGHT"])),
                      KruskalMaze(int(self.data["WIDTH"]),
                                  int(self.data["HEIGHT"])),
                      WilsonMaze(int(self.data["WIDTH"]),
                                 int(self.data["HEIGHT"]))]
        self.actual_maze = 0
        self.mazes[self.actual_maze].generate_maze()
        self.visual = VisualManager(3)
        entry_exit = self.get_entry_exit(self.data["ENTRY"], self.data["EXIT"])
        self.visual.get_visuals(self.mazes[self.actual_maze], entry_exit)
        self.default_maze()

    def get_entry_exit(self, entry: str, exit: str) -> tuple:
        lst_entry = entry.split(",")
        lst_exit = exit.split(",")
        coord_entry = (int(lst_entry[0]), int(lst_entry[1]))
        coord_exit = (int(lst_exit[0]), int(lst_exit[1]))
        return (coord_entry, coord_exit)

    def default_maze(self) -> None:
        self.visual.generate_default()

    def keyboard_management(self, keycode: int, *args: Any) -> None:
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
            self.visual.maze.maze = self.mazes[self.actual_maze]

    def looping(self) -> None:
        self.visual.mlx.mlx_key_hook(self.visual.window,
                                     self.keyboard_management, None)
        self.visual.mlx.mlx_hook(self.visual.window, 33, 0,
                                 self.visual.close_button, None)
        self.visual.mlx.mlx_loop(self.visual.ptr)


if __name__ == "__main__":
    handler = HandleMaze()
    handler.looping()
