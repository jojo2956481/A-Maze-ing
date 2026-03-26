from mlx import Mlx
import random


class Visual:
    def __init__(self):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.screen_size = self.mlx.mlx_get_screen_size(self.ptr)
        self.size_case = 0
        self.window = None
        self.colors = self.starting_colors()
        self.random_color = True

    def starting_colors(self) -> None:
        return [((227, 18, 18), (245, 107, 80)),
                ((250, 120, 15), (255, 146, 69)),
                ((255, 255, 0), (230, 228, 64)),
                ((128, 255, 0), (134, 229, 62)),
                ((0, 171, 19), (24, 121, 23)),
                ((0, 171, 134), (0, 255, 200)),
                ((0, 105, 171), (18, 85, 138)),
                ((80, 0, 171), (119, 0, 255)),
                ((171, 0, 148), (255, 0, 221)),
                ((102, 60, 14), (145, 109, 75))]

    def get_color(self) -> tuple:
        if self.random_color:
            wall = []
            background = []
            for _ in range(3):
                wall.append(random.randint(0, 255))
                background.append(random.randint(0, 255))
            return (tuple(wall), tuple(background))
        return random.choice(self.colors)

    def print_limits(self, size, limits, data, index, walls):
        color = self.actual_color
        j = index
        for n in range(len(limits)):
            for i in range(0, size * 4, 4):
                if i == 0 and (not limits[n] or not walls[n][0]):
                    data[j + i] = color[1][2]
                    data[j + i + 1] = color[1][1]
                    data[j + i + 2] = color[1][0]
                    data[j + i + 3] = 255
                elif i == size * 4 and (not limits[n] or not walls[n][1]):
                    data[j + i] = color[1][2]
                    data[j + i + 1] = color[1][1]
                    data[j + i + 2] = color[1][0]
                    data[j + i + 3] = 255
                elif not limits[n]:
                    data[j + i] = color[1][2]
                    data[j + i + 1] = color[1][1]
                    data[j + i + 2] = color[1][0]
                    data[j + i + 3] = 255
                else:
                    data[j + i] = color[0][2]
                    data[j + i + 1] = color[0][1]
                    data[j + i + 2] = color[0][0]
                    data[j + i + 3] = 255
            j += size * 4
        return j

    def print_walls(self, size, walls, data, index):
        color = self.actual_color
        j = index
        for n in range(0, size - 2):
            for cell in walls:
                i = 0
                if not cell[0]:
                    data[j + i] = color[1][2]
                    data[j + i + 1] = color[1][1]
                    data[j + i + 2] = color[1][0]
                    data[j + i + 3] = 255
                else:
                    data[j + i] = color[0][2]
                    data[j + i + 1] = color[0][1]
                    data[j + i + 2] = color[0][0]
                    data[j + i + 3] = 255
                i += 4
                while i < size * 4 - 4:
                    if False:
                        data[j + i] = color[1][2]
                        data[j + i + 1] = color[1][1]
                        data[j + i + 2] = color[1][0]
                        data[j + i + 3] = 255
                    else:
                        data[j + i] = color[0][2]
                        data[j + i + 1] = color[0][1]
                        data[j + i + 2] = color[0][0]
                        data[j + i + 3] = 255
                    i += 4
                if not cell[1]:
                    data[j + i] = color[1][2]
                    data[j + i + 1] = color[1][1]
                    data[j + i + 2] = color[1][0]
                    data[j + i + 3] = 255
                else:
                    data[j + i] = color[0][2]
                    data[j + i + 1] = color[0][1]
                    data[j + i + 2] = color[0][0]
                    data[j + i + 3] = 255
                i += 4
                j += i
        return j

    def refresh(self, maze):
        data = self.data_image[0]
        self.mlx.mlx_clear_window(self.ptr, self.window)
        index = 0
        self.actual_color = self.get_color()
        for line in maze.maze:
            ceilling = [cell["N"] for cell in line]
            walls = [(cell["W"], cell["E"]) for cell in line]
            floor = [cell["S"] for cell in line]
            index = self.print_limits(self.size_case, ceilling,
                                      data, index, walls)
            index = self.print_walls(self.size_case, walls, data, index)
            index = self.print_limits(self.size_case, floor, data,
                                      index, walls)
        self.color_forty_two(maze)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.image_maze, 10, 10)

    def create_window(self, maze) -> None:
        self.size_case = int(((self.screen_size[1] / 2) / maze.width - 1) / 2)
        self.window = self.mlx.mlx_new_window(self.ptr, int(self.size_case *
                                                            maze.width + 20),
                                              int(self.size_case * maze.height
                                                  + 20), "Maze")

    def create_maze_image(self, maze):
        self.image_maze = self.mlx.mlx_new_image(self.ptr, int(self.size_case
                                                               * maze.width),
                                                 int(self.size_case *
                                                     maze.height))
        self.data_image = self.mlx.mlx_get_data_addr(self.image_maze)

    def gere_close(self, dummy):
        self.mlx.mlx_loop_exit(self.ptr)

    def closing(self, keycode, params):
        if keycode == 113:
            self.mlx.mlx_loop_exit(self.ptr)
