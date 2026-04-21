from srcs.mazegen.maze import Maze
from typing import Any


class output_file():

    def take_arg(self, maze: Maze) -> None:
        self.height: int = maze.height
        self.width: int = maze.width
        self.maze: list[list[dict[str, Any]]] = maze.maze

    def return_exa(self) -> str:
        line: list[str] = []
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                cell = self.maze[i][j]
                binaire = ""
                binaire += '1' if cell['W'] else '0'
                binaire += '1' if cell['S'] else '0'
                binaire += '1' if cell['E'] else '0'
                binaire += '1' if cell['N'] else '0'

                row += format(int(binaire, 2), 'X')
            line.append(row)
        return "\n".join(line)

    def make_file(self, name: str, entry: int, exit: int, path: str, hexa: str) -> None:
        try:
            with open(name, "w") as f:
                f.write(hexa + "\n\n")
                f.write(str(entry) + "\n")
                f.write(str(exit) + "\n")
                f.write(path)
        except IOError as e:
            print(f"File cannot be opened : {e}")
