from .xpm.xpm_generator import create_xpm_title
from mlx import Mlx


class VisualInfo:
    def __init__(self, mlx, ptr, window, title, infos):
        self.mlx = mlx
        self.ptr = ptr
        self.string = [Mlx() for i in range(10)]
        self.window = window
        self.title_coordinate = title
        self.infos_coordinate = infos

    def print_info(self) -> None:
        self.generate_title()
        self.generate_commands()

    def generate_title(self) -> None:
        create_xpm_title("A-maze-ing", "amazing.xpm", 15)
        create_xpm_title("Commands", "commands.xpm", 5)

    def generate_commands(self):
        image = self.mlx.mlx_xpm_file_to_image(self.ptr, "amazing.xpm")
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, image[0],
                                         self.title_coordinate[0],
                                         self.title_coordinate[1])
        image = self.mlx.mlx_xpm_file_to_image(self.ptr, "commands.xpm")
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, image[0],
                                         self.infos_coordinate[0] + 10,
                                         self.infos_coordinate[1] - 40)
        self.generate_background()
        commands = ["quit: q", "change color: c", "random color: r",
                    "new maze: n", "active/stop play mode: p",
                    "change game speed: + and -", "show path: s",
                    "hide path: h"]
        i = 20
        for z in range(len(commands)):
            self.mlx.mlx_string_put(self.ptr, self.window,
                                    self.infos_coordinate[0] + 20,
                                    self.infos_coordinate[1] + i,
                                    0xFF000000, commands[z])
            i += 30

    def generate_background(self):
        temp = self.mlx.mlx_new_image(self.ptr, 300, 600)
        data = self.mlx.mlx_get_data_addr(temp)[0]
        for i in range(0, len(list(data)), 4):
            if i % 1200 <= 8 or i % 1200 >= 1187:
                data[i: i + 4] = bytearray([169, 169, 169, 255])
            elif i // 1200 <= 2 or i // 1200 >= 598:
                data[i: i + 4] = bytearray([169, 169, 169, 255])
            else:
                data[i: i + 4] = bytearray([246, 249, 250, 255])
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, temp,
                                         self.infos_coordinate[0],
                                         self.infos_coordinate[1])
