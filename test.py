import mazegen

if __name__ == "__main__":
    maze = mazegen.DfsMaze(5, 5, (0, 0), None, True)
    maze.generate_maze()
    print(maze.maze)