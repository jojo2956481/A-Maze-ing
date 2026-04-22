import mazegen.dfs_iterative as dfs
from srcs.mazegen.solver import solver_test


if __name__ == "__main__":
    maze = dfs.DfsMaze(400, 400, ((0, 0), (199, 199)), None, True)
    maze.generate_maze()
    solver_test(((0, 0), (40, 40)), maze)
