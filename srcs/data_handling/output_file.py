from srcs.mazegen.maze import Maze
from typing import Any


class output_file():
    """
    class for the output file method
    """

    def take_arg(self, maze: Maze) -> None:
        """
        takes the maze attributes for the class methods
        """
        self.height: int = maze.height
        self.width: int = maze.width
        self.entry = maze.entry
        self.exit = maze.exit
        self.maze: list[list[dict[str, Any]]] = maze.maze

    def return_exa(self) -> str:
        """
        convert the cells of the maze from binary to hexadecimal
        """
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

    def make_file(self, name: str, path: str, hexa: str) -> None:
        """
        method to create the output file and write data
        """
        try:
            with open(name, "w") as f:
                f.write(hexa + "\n\n")
                f.write(str(self.entry) + "\n")
                f.write(str(self.exit) + "\n")
                f.write(path)
        except IOError as e:
            print(f"File cannot be opened : {e}")


def create_file(maze: Maze, name: str, path: str):
    """
    function to manage all method to create output file
    """
    file = output_file()
    file.take_arg(maze)
    hexa = file.return_exa()
    file.make_file(name, path, hexa)


