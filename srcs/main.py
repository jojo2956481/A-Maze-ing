from algo.wilson_iterative import Maze
from parsing.visual import Visual
import parsing.parsing as parsing


if __name__ == "__main__":
    parsed_data = parsing.pars_dict()
    maze = Maze(int(parsed_data["WIDTH"]), int(parsed_data["HEIGHT"]))
    m = Visual()
    maze.generate_maze()
    m.create_window(maze)
    m.create_maze_image(maze)
    m.refresh(maze)
    m.mlx.mlx_key_hook(m.window, m.closing, None)
    m.mlx.mlx_hook(m.window, 33, 0, m.gere_close, None)
    m.mlx.mlx_loop(m.ptr)
