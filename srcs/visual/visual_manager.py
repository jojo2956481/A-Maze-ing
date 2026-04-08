from mlx import Mlx
from .visual_info import VisualInfo
from .visual_maze import VisualMaze
from .visual_path import VisualPath
from .visual_play import VisualPlay
from algo.solver import solver_all_path


class VisualManager:
    def __init__(self):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.handle_screen_size()
        self.window = self.mlx.mlx_new_window(self.ptr,
                                              self.screen["window"][0],
                                              self.screen["window"][1],
                                              "A-maze-ing")

    def handle_screen_size(self):
        screen_size = self.mlx.mlx_get_screen_size(self.ptr)
        self.screen = {
            "window": (int(screen_size[1] // 2.5 * 1.5),
                       int(screen_size[2] // 1.8 * 1.5))
        }
        self.screen["maze"] = (((self.screen["window"][0] // 3) * 2,
                                (self.screen["window"][1] // 3) * 2),
                               (self.screen["window"][0] // 15,
                                self.screen["window"][1] // 6))
        self.screen["info"] = (self.screen["window"][0] // 5,
                               self.screen["window"][1] // 15)
        self.screen["title"] = (int(self.screen["window"][0] * 0.73),
                                int(self.screen["window"][1] // 3))
        print(screen_size, self.screen)

    def get_visuals(self, maze, entry_exit) -> None:
        paths = [[value[0] for value in path] for path in
                 solver_all_path(entry_exit, maze)]
        self.maze = VisualMaze(maze, self.mlx, self.ptr,
                               self.window, self.screen["maze"], entry_exit)
        self.info = VisualInfo(self.mlx, self.ptr, self.window,
                               self.screen["info"], self.screen["title"])
        self.path = VisualPath(self.mlx, self.ptr, self.window,
                               self.screen["maze"][1],
                               paths, maze, self.maze)
        self.play = VisualPlay(self.mlx, self.ptr, self.window, maze,
                               self.maze.size_case, entry_exit,
                               self.screen["maze"][1],
                               self.maze)

    def generate_default(self):
        self.info.print_info()
        self.maze.create_maze_image()
        self.maze.refresh()

    def gere_close(self, dummy):
        self.mlx.mlx_loop_exit(self.ptr)

    def closing(self, keycode, params):
        if keycode == 113:
            self.mlx.mlx_loop_exit(self.ptr)
        if keycode == 99:
            self.maze.get_color()
            self.maze.refresh()
        if keycode == 110:
            self.maze.maze.generate_maze()
            self.path.paths = [[value[0] for value in path] for path in
                               solver_all_path(self.maze.entry_exit,
                                               self.maze.maze)]
            self.maze.refresh()
        if keycode == 114:
            self.maze.random_color = not self.maze.random_color
        if keycode == 112:
            self.mlx.mlx_loop_hook(self.ptr, self.play.play, None)
            self.play.playmod = not self.play.playmod
            self.maze.show_to_window()
        if keycode == 61:
            self.play.game_speed = min(5, self.play.game_speed + 1)
        if keycode == 45:
            self.play.game_speed = max(1, self.play.game_speed - 1)
        if keycode == 115:
            self.path.show_path()
        if keycode == 104:
            self.maze.refresh()
        if keycode == 105:
            self.path.speed = 1 if self.path.speed == 0 else 0
        if keycode == 65361:
            self.path.speed = self.path.speed - 1 if self.path.speed > 0 else 1
        if keycode == 65363:
            self.path.speed = self.path.speed + 1 if self.path.speed < 6 else 5
        if keycode == 65362:
            if self.path.actual_path + 1 < len(self.path.paths):
                self.path.actual_path += 1
            else:
                self.path.actual_path = 0
        if keycode == 65364:
            if self.path.actual_path - 1 > 0:
                self.path.actual_path -= 1
            else:
                self.path.actual_path = len(self.path.paths - 1)
