from mlx import Mlx
from typing import Any
from srcs.mazegen.maze import Maze
from srcs.visual.visual_maze import VisualMaze
from time import time


class VisualPath:
    """
    class that handle the visual of the paths
    """
    def __init__(self, mlx: Mlx, ptr: Any, window: Any,
                 coordinate: tuple[int, int],
                 paths: list[list[tuple[int, int]]],
                 maze: Maze, visual: VisualMaze) -> None:
        """
        instantiate the mlx, the paths and the maze
        """
        self.mlx = mlx
        self.ptr = ptr
        self.window = window
        self.coordinate = coordinate
        self.paths = paths
        self.actual_path = 0
        self.maze = maze
        self.speed = 0
        self.visual = visual
        self.frame: int = 0
        self.delay: float = 0
        self.show = False

    def slow_path(self, data: memoryview) -> None:
        """
        print the solution at a speed depending of the given speed
        """
        try:
            cell = self.paths[self.actual_path][self.cell]
        except IndexError:
            self.mlx.mlx_loop_hook(self.ptr, None, None)
            return
        if time() - self.delay < 0.4 - (self.speed * 0.07):
            return
        color = bytearray([255, 255, 255, 255])
        cell = self.paths[self.actual_path][self.cell]
        size_line = self.visual.size_case * len(self.maze.maze[0]) * 4
        pos = (size_line * self.visual.size_case *
               cell[1]) + (self.visual.size_case * cell[0] * 4)
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
        self.delay = time()
        self.cell += 1

    def show_path(self, data: memoryview) -> None:
        """
        print the paths
        """
        color = bytearray([255, 255, 255, 255])
        for cell in self.paths[self.actual_path]:
            size_line = self.visual.size_case * len(self.maze.maze[0]) * 4
            pos = (size_line * self.visual.size_case *
                   cell[1]) + (self.visual.size_case * cell[0] * 4)
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
        """
        handle the instante mode or slow mode
        """
        data = self.visual.data_image[0]
        self.delay = time() - 1
        self.cell: int = 0
        if self.speed:
            self.mlx.mlx_loop_hook(self.ptr, self.slow_path, data)
        else:
            self.show_path(data)
