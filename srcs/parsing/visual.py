from mlx import Mlx
import random


class Visual:
    def __init__(self, maze):
        self.maze = maze
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.screen_size = self.mlx.mlx_get_screen_size(self.ptr)
        self.size_case = 0
        self.window = None
        self.colors = self.starting_colors()
        self.random_color = False
        self.get_color()

    def starting_colors(self) -> None:
        return [("0xFF00FFFF", "0xFF7393B3"),  # Aqua / Blue Gray
                ("0xFF0F52BA", "0xFF87CEEB"),  # Saphire Blue / Sky Blue
                ("0xFF800020", "0xFFE97451"),  # Burgundy / Burnt Sienna
                ("0xFF36454F", "0xFFE5E4E2"),  # Charcoal / Platinum
                ("0xFF228B22", "0xFF355E3B"),  # Forest Green / Hunter Green
                ("0xFFF28C28", "0xFF8B4000"),  # Cadamium Orange / Dark Orange
                ("0xFFF33A6A", "0xFF811331"),  # Rose / Claret
                ("0xFF5D3FD3", "0xFFCBC3E3"),  # Iris / Light purple
                ("0xFFFF2400", "0xFF800000"),  # Scarlet / Maroon
                ("0xFFDAA520", "0xFFFFDEAD")]  # Goldenrod / Navajo White

    def get_color(self) -> None:
        if self.random_color:
            color_hexa = (hex(random.randrange(0xFF000000, 0xFFFFFFFF)),
                          hex(random.randrange(0xFF000000, 0xFFFFFFFF)))
        else:
            color_hexa = random.choice(self.colors)
        temp = (bytearray([int(f"0x{color_hexa[0][i: i+2]}", 16)
                           for i in range(len(color_hexa[0]) - 2, 0, -2)]),
                bytearray([int(f"0x{color_hexa[1][i: i+2]}", 16)
                           for i in range(len(color_hexa[1]) - 2, 0, -2)]))
        try:
            if temp == self.actual_color:
                self.get_color()
                return
            else:
                self.actual_color = temp
        except AttributeError:
            self.actual_color = temp

    def print_limits(self, size, limits, data, index, walls):
        j = index
        for n in range(len(limits)):
            for i in range(0, size * 4, 4):
                if i == 0 and (not limits[n] or not walls[n][0]):
                    data[j: j + 4] = self.actual_color[0]
                elif i == size * 4 - 4 and (not limits[n] or not walls[n][1]):
                    data[j + i: j + i + 4] = self.actual_color[0]
                elif not limits[n]:
                    data[j + i: j + i + 4] = self.actual_color[0]
                else:
                    data[j + i: j + i + 4] = self.actual_color[1]
            j += size * 4
        return j

    def print_walls(self, size, walls, data, index):
        j = index
        for n in range(0, size - 2):
            for cell in walls:
                i = 0
                if not cell[0]:
                    data[j: j + 4] = self.actual_color[0]
                else:
                    data[j: j + 4] = self.actual_color[1]
                i += 4
                while i < size * 4 - 4:
                    data[j + i: j + i + 4] = self.actual_color[1]
                    i += 4
                if not cell[1]:
                    data[j + i: j + i + 4] = self.actual_color[0]
                else:
                    data[j + i: j + i + 4] = self.actual_color[1]
                i += 4
                j += i
        return j

    def color_forty_two(self) -> None:
        image = self.mlx.mlx_new_image(self.ptr, self.size_case,
                                       self.size_case)
        image_info = self.mlx.mlx_get_data_addr(image)[0]
        for i in range(0, self.size_case ** 2 * 4, 4):
            image_info[i: i + 4] = self.actual_color[0]
        for cell in self.maze.forty_two:
            self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                             image, 10 +
                                             cell[1] * self.size_case,
                                             cell[0] * self.size_case + 10)

    def refresh(self):
        data = self.data_image[0]
        self.mlx.mlx_clear_window(self.ptr, self.window)
        index = 0
        for line in self.maze.maze:
            ceilling = [cell["N"] for cell in line]
            walls = [(cell["W"], cell["E"]) for cell in line]
            floor = [cell["S"] for cell in line]
            index = self.print_limits(self.size_case, ceilling,
                                      data, index, walls)
            index = self.print_walls(self.size_case, walls, data, index)
            index = self.print_limits(self.size_case, floor, data,
                                      index, walls)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.image_maze, 10, 10)
        self.color_forty_two()

    def create_window(self) -> None:
        self.size_case = int(((self.screen_size[1] / 2)
                              / self.maze.width - 1) / 2)
        self.window = self.mlx.mlx_new_window(self.ptr, int(self.size_case *
                                                            self.maze.width
                                                            + 20),
                                              int(self.size_case *
                                                  self.maze.height
                                                  + 20), "Maze")

    def create_maze_image(self):
        self.image_maze = self.mlx.mlx_new_image(self.ptr,
                                                 int(self.size_case
                                                     * self.maze.width),
                                                 int(self.size_case *
                                                     self.maze.height))
        self.data_image = self.mlx.mlx_get_data_addr(self.image_maze)

    def gere_close(self, dummy):
        self.mlx.mlx_loop_exit(self.ptr)

    def closing(self, keycode, params):
        if keycode == 113:
            self.mlx.mlx_loop_exit(self.ptr)
        if keycode == 99:
            self.get_color()
            self.refresh()
        if keycode == 110:
            self.maze.generate_maze()
            self.refresh()
        if keycode == 114:
            self.random_color = not self.random_color
