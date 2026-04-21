from srcs.visual.xpm.xpm_generator import create_xpm_title
from mlx import Mlx
from typing import Any


class VisualInfo:
    def __init__(self, mlx: Mlx, ptr: Any, window: Any,
                 title: tuple[tuple[int, int], int],
                 infos: tuple[int, int]) -> None:
        self.mlx = mlx
        self.ptr = ptr
        self.window = window
        self.title_coordinate = title[0]
        self.title_size = title[1]
        self.infos_coordinate = infos

    def print_info(self) -> None:
        self.generate_title()
        self.generate_commands()

    def generate_title(self) -> None:
        create_xpm_title("A-maze-ing", "amazing.xpm", self.title_size)
        create_xpm_title("Commands", "commands.xpm", 5)

    def generate_commands(self) -> None:
        image = self.mlx.mlx_xpm_file_to_image(self.ptr, "amazing.xpm")
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, image[0],
                                         self.title_coordinate[0],
                                         self.title_coordinate[1])
        image = self.mlx.mlx_xpm_file_to_image(self.ptr, "commands.xpm")
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, image[0],
                                         self.infos_coordinate[0] + 10,
                                         self.infos_coordinate[1] - 40)
        self.generate_background()
        self.mlx.mlx_do_sync(self.ptr)
        commands = ["quit: q", "change color: c", "random color: r",
                    "new maze: n", "active/stop play mode: p",
                    "change game speed: + and -", "show path: s",
                    "hide path: h", "previous solution:", "   - up arrow",
                    "next solution:", "   - down arrow",
                    "active/stop instant path: i", "higher path speed:",
                    "   - right arrow", "lower path speed:", "   - left arrow",
                    "DFS: 1", "Kruskal: 2", "Wilson: 3"]
        i = 30
        for z in range(len(commands)):
            self.mlx.mlx_string_put(self.ptr, self.window,
                                    self.infos_coordinate[0] + 20,
                                    self.infos_coordinate[1] + i,
                                    0, commands[z])
            i += 27

    def generate_background(self) -> None:
        temp = self.mlx.mlx_new_image(self.ptr, 300, 600)
        data = self.mlx.mlx_get_data_addr(temp)[0]
        for i in range(0, 300 * 600 * 4, 4):
            if i % 1200 <= 8 or i % 1200 >= 1187:
                data[i: i + 4] = bytearray([169, 169, 169, 255])
            elif i // 1200 <= 2 or i // 1200 >= 598:
                data[i: i + 4] = bytearray([169, 169, 169, 255])
            else:
                data[i: i + 4] = bytearray([246, 249, 250, 255])
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, temp,
                                         self.infos_coordinate[0],
                                         self.infos_coordinate[1])
