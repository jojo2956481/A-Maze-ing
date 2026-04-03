from time import sleep


class VisualPath:
    def __init__(self, mlx, ptr, window, coordinate, paths,
                 maze, visual):
        self.mlx = mlx
        self.ptr = ptr
        self.window = window
        self.coordinate = coordinate
        self.paths = [[value[0] for value in path] for path in paths]
        self.actual_path = 0
        self.maze = maze
        self.speed = 0
        self.visual = visual

    def show_path(self, color=None):
        data = self.visual.data_image[0]
        if not color:
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
            if self.speed:
                sleep()
                self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                                 self.visual.image_maze,
                                                 self.coordinate[0],
                                                 self.coordinate[1])
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.visual.image_maze,
                                         self.coordinate[0],
                                         self.coordinate[1])
