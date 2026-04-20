from mlx import Mlx
from srcs.visual.visual_info import VisualInfo
from srcs.visual.visual_maze import VisualMaze
from srcs.visual.visual_path import VisualPath
from srcs.visual.visual_play import VisualPlay
from srcs.mazegen.solver import solver_all_path
from srcs.mazegen.maze import Maze
from typing import Any
from enum import Enum


class Commands(Enum):
    QUIT = 113
    NEXT_COLOR = 99
    NEW_MAZE = 110
    RANDOM_COLOR = 114
    PLAYMODE = 112
    GAME_SPEED_HIGH = 61
    GAME_SPEED_LOW = 45
    SHOW_PATH = 115
    HIDE_PATH = 104
    INSTANT_MODE = 105
    PREV_PATH = 65362
    NEXT_PATH = 65364
    PATH_SPEED_HIGH = 65363
    PATH_SPEED_LOW = 65361


class VisualManager:
    def __init__(self, window_size: int) -> None:
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.handle_screen_size(window_size)
        self.window = self.mlx.mlx_new_window(self.ptr,
                                              self.screen["window"][0],
                                              self.screen["window"][1],
                                              "A-maze-ing")

    def handle_screen_size(self, window_size: int) -> None:
        screen_size = self.mlx.mlx_get_screen_size(self.ptr)
        self.screen: dict[str, Any] = {
            "window": (int(screen_size[1] // 2.5 * (1 + 0.4 *
                                                    (window_size - 1))),
                       int(screen_size[2] // 1.8 * (1 + 0.4 *
                                                    (window_size - 1))))
        }
        self.screen["maze"] = (((self.screen["window"][0] // 3) * 2 - 100,
                                (self.screen["window"][1] // 3) * 2 - 100),
                               (self.screen["window"][0] // 15,
                                self.screen["window"][1] // 6))
        self.screen["info"] = (self.screen["maze"][1][0] + 100 +
                               (self.screen["maze"][0][0]),
                               self.screen["maze"][1][1] +
                               (self.screen["maze"][0][0] // 2) - 300)
        self.screen["title"] = ((int(self.screen["window"][0] // 2) -
                                (int(self.screen["window"][0] // 100) * 27),
                                self.screen["window"][1] // 18),
                                self.screen["window"][0] // 100)

    def get_visuals(self, maze: Maze,
                    entry_exit: tuple[tuple[int, int],
                                      tuple[int, int]]) -> None:
        paths = [[value[0] for value in path] for path in
                 solver_all_path(entry_exit, maze)]
        self.maze = VisualMaze(maze, self.mlx, self.ptr,
                               self.window, self.screen["maze"], entry_exit)
        self.info = VisualInfo(self.mlx, self.ptr, self.window,
                               self.screen["title"], self.screen["info"])
        self.path = VisualPath(self.mlx, self.ptr, self.window,
                               self.screen["maze"][1],
                               paths, maze, self.maze)
        self.play = VisualPlay(self.mlx, self.ptr, self.window, maze,
                               self.maze.size_case, entry_exit,
                               self.screen["maze"][1],
                               self.maze)

    def generate_default(self) -> None:
        self.info.print_info()
        self.maze.create_maze_image()
        self.maze.refresh()

    def close_button(self, args: Any) -> None:
        self.mlx.mlx_loop_exit(self.ptr)

    def keyboard_management(self, keycode: int) -> None:
        match keycode:
            case Commands.QUIT.value:
                self.mlx.mlx_loop_exit(self.ptr)
            case Commands.NEXT_COLOR.value:
                self.maze.get_color()
                self.maze.refresh()
            case Commands.NEW_MAZE.value:
                self.maze.maze.generate_maze()
                self.path.paths = [[value[0] for value in path] for path in
                                   solver_all_path(self.maze.entry_exit,
                                                   self.maze.maze)]
                self.maze.refresh()
            case Commands.RANDOM_COLOR.value:
                self.maze.random_color = not self.maze.random_color
            case Commands.PLAYMODE.value:
                self.mlx.mlx_loop_hook(self.ptr, self.play.play, None)
                self.play.playmod = not self.play.playmod
                self.maze.show_to_window()
            case Commands.GAME_SPEED_HIGH.value:
                self.play.game_speed = min(5, self.play.game_speed + 1)
            case Commands.GAME_SPEED_LOW.value:
                self.play.game_speed = max(1, self.play.game_speed - 1)
            case Commands.SHOW_PATH.value:
                self.maze.refresh()
                self.path.handle_path()
            case Commands.HIDE_PATH.value:
                self.path.cell = len(self.path.paths[self.path.actual_path])
                self.maze.refresh()
            case Commands.INSTANT_MODE.value:
                self.path.speed = 1 if self.path.speed == 0 else 0
            case Commands.PATH_SPEED_LOW.value:
                if self.path.speed > 1:
                    self.path.speed -= 1
            case Commands.PATH_SPEED_HIGH.value:
                if self.path.speed < 5:
                    self.path.speed += 1
            case Commands.PREV_PATH.value:
                if self.path.actual_path - 1 > 0:
                    self.path.actual_path -= 1
                else:
                    self.path.actual_path = len(self.path.paths) - 1
            case Commands.NEXT_PATH.value:
                if self.path.actual_path + 1 < len(self.path.paths):
                    self.path.actual_path += 1
                else:
                    self.path.actual_path = 0
