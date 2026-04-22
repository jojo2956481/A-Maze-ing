from mlx import Mlx
from typing import Any
from srcs.mazegen.maze import Maze
from srcs.visual.visual_maze import VisualMaze


class VisualPlay:
    """
    class that handle the play mode
    """
    def __init__(self, mlx: Mlx, ptr: Any, window: Any, maze: Maze,
                 size_case: int,
                 entry_exit: tuple[tuple[int, int], tuple[int, int]],
                 maze_coordinate: tuple[int, int],
                 visual_maze: VisualMaze) -> None:
        """
        instantiate mlx, coordinate and maze
        """
        self.mlx = mlx
        self.ptr = ptr
        self.window = window
        self.maze = maze
        self.maze_coordinate = maze_coordinate
        self.size_case = size_case
        self.coordinate = (entry_exit[0][0] + 1, entry_exit[0][1] + 1)
        self.entry_exit = entry_exit
        self.create_player()
        self.visual_maze = visual_maze
        self.playmod = False
        self.game_speed = 1

    def create_player(self) -> None:
        """
        create a image for the player
        """
        self.size = int(self.size_case * 0.7)
        self.player = self.mlx.mlx_new_image(self.ptr, self.size,
                                             self.size)
        data = self.mlx.mlx_get_data_addr(self.player)[0]
        for i in range(0, len(list(data)), 4):
            data[i: i + 4] = bytearray([52, 52, 52, 255])

    def is_in_maze(self, mouse: tuple[int, int]) -> bool:
        """
        check if the mouse is in the maze
        """
        try:
            if (mouse[0] >= 0 and
                    mouse[0] <= self.maze_len[0] * self.size_case and
                mouse[1] >= 0
                    and mouse[1] <= self.maze_len[1] * self.size_case):
                return True
            return False
        except Exception:
            self.maze_len: tuple[int, int] = (len(self.maze.maze[0]),
                                              len(self.maze.maze))
            return self.is_in_maze(mouse)

    def get_direction(self, mouse: tuple[int, int]) -> str:
        """
        determine the position the player should go, depending on the
        mouse position and the player position
        """
        new_pos = ((mouse[0] - self.coordinate[0]) - self.size // 2,
                   (mouse[1] - self.coordinate[1]) - self.size // 2)
        if abs(new_pos[0]) > abs(new_pos[1]):
            if new_pos[0] >= 0:
                direction = "E"
            else:
                direction = "W"
        else:
            if new_pos[1] >= 0:
                direction = "S"
            else:
                direction = "N"
        return direction

    def check_north(self, new_pos: tuple[int, int]) -> bool:
        """
        check if the player can go to the north
        """
        corners = ((new_pos[0], new_pos[1]),
                   (new_pos[0] + self.size - 1, new_pos[1]))
        cells = (self.maze.maze[int(corners[0][1] / self.size_case)]
                 [int(corners[0][0] / self.size_case)],
                 self.maze.maze[int(corners[1][1] / self.size_case)]
                 [int(corners[1][0] / self.size_case)])
        walls = (cells[0]["N"], cells[1]["N"], cells[0]["E"])
        if not (walls[0] and walls[1]):
            if corners[0][1] % self.size_case == 0:
                return False
        if not walls[2] and (corners[0][0] // self.size_case !=
                             corners[1][0] // self.size_case):
            return False
        if (corners[0][0] % self.size_case == 0 and not cells[0]["W"]):
            return False
        if (corners[1][0] % self.size_case == self.size_case - 1 and
                not cells[1]["E"]):
            return False
        return True

    def check_est(self, new_pos: tuple[int, int]) -> bool:
        """
        check if the player can go to the est
        """
        corners = ((new_pos[0] + self.size - 1, new_pos[1]),
                   (new_pos[0] + self.size - 1, new_pos[1] + self.size - 1))
        cells = (self.maze.maze[int(corners[0][1] / self.size_case)]
                 [int(corners[0][0] / self.size_case)],
                 self.maze.maze[int(corners[1][1] / self.size_case)]
                 [int(corners[1][0] / self.size_case)])
        walls = (cells[0]["E"], cells[1]["E"], cells[0]["S"])
        if not (walls[0] and walls[1]):
            if corners[0][0] % self.size_case == self.size_case - 1:
                return False
        if not walls[2] and (corners[0][1] // self.size_case !=
                             corners[1][1] // self.size_case):
            return False
        if (corners[0][1] % self.size_case == 0 and not cells[0]["N"]):
            return False
        if (corners[1][1] % self.size_case == self.size_case - 1 and
                not cells[1]["S"]):
            return False
        return True

    def check_south(self, new_pos: tuple[int, int]) -> bool:
        """
        check if the player can go to the south
        """
        corners = ((new_pos[0], new_pos[1] + self.size - 1),
                   (new_pos[0] + self.size - 1, new_pos[1] + self.size - 1))
        cells = (self.maze.maze[int(corners[0][1] / self.size_case)]
                 [int(corners[0][0] / self.size_case)],
                 self.maze.maze[int(corners[1][1] / self.size_case)]
                 [int(corners[1][0] / self.size_case)])
        walls = (cells[0]["S"], cells[1]["S"], cells[0]["E"])
        if not (walls[0] and walls[1]):
            if corners[0][1] % self.size_case == self.size_case - 1:
                return False
        if not walls[2] and (corners[0][0] // self.size_case !=
                             corners[1][0] // self.size_case):
            return False
        if (corners[0][0] % self.size_case == 0 and not cells[0]["W"]):
            return False
        if (corners[1][0] % self.size_case == self.size_case - 1 and
                not cells[1]["E"]):
            return False
        return True

    def check_west(self, new_pos: tuple[int, int]) -> bool:
        """
        check if the player can go to the west
        """
        corners = ((new_pos[0], new_pos[1]),
                   (new_pos[0], new_pos[1] + self.size - 1))
        cells = (self.maze.maze[int(corners[0][1] / self.size_case)]
                 [int(corners[0][0] / self.size_case)],
                 self.maze.maze[int(corners[1][1] / self.size_case)]
                 [int(corners[1][0] / self.size_case)])
        walls = (cells[0]["W"], cells[1]["W"], cells[0]["S"])
        if not (walls[0] and walls[1]):
            if corners[0][0] % self.size_case == 0:
                return False
        if not walls[2] and (corners[0][1] // self.size_case !=
                             corners[1][1] // self.size_case):
            return False
        if (corners[0][1] % self.size_case == 0 and not cells[0]["N"]):
            return False
        if (corners[1][1] % self.size_case == self.size_case - 1 and
                not cells[1]["S"]):
            return False
        return True

    def new_pos_valid(self, new_pos: tuple[int, int], direction: str) -> bool:
        """
        call the check method depending of the direction
        """
        if direction == "N":
            return self.check_north(new_pos)
        elif direction == "E":
            return self.check_est(new_pos)
        elif direction == "S":
            return self.check_south(new_pos)
        else:
            return self.check_west(new_pos)

    def move_player(self, direction: str) -> None:
        """
        determine the new player position of the move
        """
        if direction == "N":
            new_pos = (self.coordinate[0], self.coordinate[1] - 1)
        elif direction == "E":
            new_pos = (self.coordinate[0] + 1, self.coordinate[1])
        elif direction == "S":
            new_pos = (self.coordinate[0], self.coordinate[1] + 1)
        else:
            new_pos = (self.coordinate[0] - 1, self.coordinate[1])
        if self.new_pos_valid(new_pos, direction):
            self.coordinate = new_pos

    def play(self, params: Any) -> None:
        """
        check if play mode is active
        try to move the player if posible and print the player to window
        """
        if self.playmod and self.size <= self.size_case - 2:
            for i in range(self.game_speed):
                _, x, y = self.mlx.mlx_mouse_get_pos(self.window)
                mouse = (x - self.maze_coordinate[0],
                         y - self.maze_coordinate[1])
                if self.is_in_maze(mouse):
                    direction = self.get_direction(mouse)
                    self.move_player(direction)
            self.visual_maze.show_to_window()
            self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                             self.player,
                                             self.coordinate[0] +
                                             self.maze_coordinate[0],
                                             self.coordinate[1] +
                                             self.maze_coordinate[1])
