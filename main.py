from maze import *
from pacman import *

maze = buildMaze()

printMaze(maze, pacmanState)
updatePacmanPosition(maze, pacmanState, [1,1])
printMaze(maze, pacmanState)
updatePacmanPosition(maze, pacmanState, [1,2])
printMaze(maze, pacmanState)
updatePacmanPosition(maze, pacmanState, [1,3])
printMaze(maze, pacmanState)
updatePacmanPosition(maze, pacmanState, [1,4])
printMaze(maze, pacmanState)
updatePacmanPosition(maze, pacmanState, [2,4])
printMaze(maze, pacmanState)
updatePacmanPosition(maze, pacmanState, [1,4])
printMaze(maze, pacmanState)
updatePacmanPosition(maze, pacmanState, [1,3])
printMaze(maze, pacmanState)