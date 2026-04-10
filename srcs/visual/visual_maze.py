import random
from algo.maze import Maze
from mlx import Mlx
from typing import Any


class VisualMaze():
    def __init__(self, maze: Maze, mlx: Mlx, ptr: Any, window: Any,
                 value: tuple[tuple[int, int], tuple[int, int]],
                 entry_exit: tuple[tuple[int, int], tuple[int, int]]) -> None:
        self.maze = maze
        self.mlx = mlx
        self.ptr = ptr
        self.define_size_case(value[0])
        self.window = window
        self.colors = self.starting_colors()
        self.random_color = False
        self.get_color()
        self.coordinate = value[1]
        self.entry_exit = entry_exit

    def starting_colors(self) -> list[tuple[str, str]]:
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

    def print_limits(self, size: int, limits: list[bool], data: memoryview,
                     index: int, walls: list[tuple[bool, bool]]) -> int:
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

    def print_walls(self, size: int, walls: list[tuple[bool, bool]],
                    data: memoryview, index: int) -> int:
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
        data = self.data_image[0]
        size_line = self.size_case * len(self.maze.maze[0]) * 4
        for case in self.maze.forty_two:
            index = (size_line * self.size_case * case[0]) + (self.size_case *
                                                              case[1] * 4)
            for i in range(self.size_case):
                for i in range(0, self.size_case * 4, 4):
                    data[index + i: index + i + 4] = self.actual_color[0]
                index += size_line

    def refresh(self) -> None:
        data = self.data_image[0]
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
        self.show_to_window()

    def put_entry_exit(self, cell: tuple[int, int],
                       color: list[int, int, int, int]) -> None:
        data = self.data_image[0]
        size_line = self.size_case * len(self.maze.maze[0]) * 4
        index = (size_line * self.size_case * cell[0]) + (self.size_case *
                                                          cell[1] * 4)
        for i in range(self.size_case):
            for i in range(0, self.size_case * 4, 4):
                if data[index + i: index + i + 4] == self.actual_color[1]:
                    data[index + i: index + i + 4] = bytearray(color)
            index += size_line

    def show_to_window(self) -> None:
        self.color_forty_two()
        self.put_entry_exit(self.entry_exit[0], [0, 255, 0, 255])
        self.put_entry_exit(self.entry_exit[1], [0, 0, 255, 255])
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.image_maze, self.coordinate[0],
                                         self.coordinate[1])

    def define_size_case(self, size_maze) -> None:
        self.size_case = int(size_maze[0]
                             / self.maze.width)

    def create_maze_image(self) -> None:
        self.image_maze = self.mlx.mlx_new_image(self.ptr,
                                                 int(self.size_case
                                                     * self.maze.width),
                                                 int(self.size_case *
                                                     self.maze.height))
        self.data_image = self.mlx.mlx_get_data_addr(self.image_maze)
