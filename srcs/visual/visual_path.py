from mlx import Mlx
from typing import Any
from algo.maze import Maze
from .visual_maze import VisualMaze


class VisualPath:
    def __init__(self, mlx: Mlx, ptr: Any, window: Any,
                 coordinate: tuple[int, int],
                 paths: list[list[tuple[int, int]]],
                 maze: Maze, visual: VisualMaze) -> None:
        self.mlx = mlx
        self.ptr = ptr
        self.window = window
        self.coordinate = coordinate
        self.paths = paths
        self.actual_path = 0
        self.maze = maze
        self.speed = 0
        self.visual = visual

    def slow_path(self, data: memoryview) -> None:
        try:
            cell = self.paths[self.actual_path][self.cell]
        except IndexError:
            self.mlx.mlx_loop_hook(self.ptr, None, None)
            return
        if self.frame != 10 - self.speed * 2:
            self.frame += 1
            return
        color = bytearray([255, 255, 255, 255])
        cell = self.paths[self.actual_path][self.cell]
        size_line = self.visual.size_case * len(self.maze.maze[0]) * 4
        pos = (size_line * self.visual.size_case *
               cell[0]) + (self.visual.size_case * cell[1] * 4)
        for i in range(self.visual.size_case):
            for i in range(0, self.visual.size_case * 4, 4):
                if (data[pos + i: pos + i + 4] ==
                        self.visual.actual_color[1]):
                    data[pos + i: pos + i + 4] = color
            pos += size_line
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.visual.image_maze,
                                         self.coordinate[0],
                                         self.coordinate[1])
        self.cell += 1
        self.frame = 0

    def show_path(self, data: memoryview) -> None:
        color = bytearray([255, 255, 255, 255])
        for cell in self.paths[self.actual_path]:
            size_line = self.visual.size_case * len(self.maze.maze[0]) * 4
            pos = (size_line * self.visual.size_case *
                   cell[0]) + (self.visual.size_case * cell[1] * 4)
            for i in range(self.visual.size_case):
                for i in range(0, self.visual.size_case * 4, 4):
                    if (data[pos + i: pos + i + 4] ==
                            self.visual.actual_color[1]):
                        data[pos + i: pos + i + 4] = color
                pos += size_line
            self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                             self.visual.image_maze,
                                             self.coordinate[0],
                                             self.coordinate[1])

    def handle_path(self) -> None:
        data = self.visual.data_image[0]
        if self.speed:
            self.frame = 0
            self.cell = 0
            self.mlx.mlx_loop_hook(self.ptr, self.slow_path, data)
        else:
            self.show_path(data)
