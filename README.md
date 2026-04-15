*This project has been created as part of the 42 curriculum by lebeyssa, eel-kerc.*


## Descripton

**A-maze-ing** is a maze generation project.  
Any algorithm can be used to generate and solve the maze.  
Maze configuration is parsed in a .txt file.  
Maze informations is then stored in a output_maze.txt.  
The maze algorithm can be transform in a .whl to be reuse in other projects that requires maze. 


## Instructions

 To run this project, you should install the required dependencies with the following command : *make install*.  
It is recommanded to use a virtual environment for dependencies installation.   
Then, you can run with the command *make run*.

 To create the .whl and .tar, run the command *make build*.

 For norm and typing checking, run *make lint*, or *make lint-strict* for strict checking.

 Run *make clean* to clean dependencies like pycache or created files.

 To run the project in debug mode using python built-in debugger, run *make debug*.


## Projects choices

- config format
- mazes generations and algorithms
- why the algorithms
- project reusability
- project management:
   - role of each member
   - project planning
   - what is working well and what can be improved
   - tools used descriptions


## Additionnal features management

### - Multiple algorithms management

The default algorithm is set to DFS. It can be change with keyboard interaction. The change work with indexes of the list of the algorithms, making it easy to add more algorithms.

### - Play mode

The play mode can be enable or disable with the keyboard (see commands when running).  
It works with mouse postion. It gets the position and find out which direction is the most dominant to move the square.  
Each direction has a wall check. Every check works the same way :
 - The program get the 2 corners leading to the direction (ex: north east and north west if going to the north)
 - It gets the position of the corners in the maze and the walls that requires checks
 - It finally checks if the corners coordinates are in the walls coordinates, to enable slice over differents cells.

### - Solution display

The default solution display is set to the quickest path.  
If the maze is set to not perfect, all possibles solutions can be displayed.  
There is a instant mode that can be enable/disable. If disable, the speed can be modified (see commands when running)


## Resources

Mermaid : https://mermaid.ai/open-source/intro/getting-started.html

### AI Usage

 - mlx installation comprehension
 - infinite loop debug
 - wilson algorithm comprehension
