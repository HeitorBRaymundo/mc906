from maze import *
from pacman import *

maze = buildMaze(pacmanState)

printMaze(maze, pacmanState)
possibleActions = getPossibleActions(maze, pacmanState)

nextPosition = possibleActions[0]

while(nextPosition):
  updatePacmanPosition(maze, pacmanState, nextPosition['pos'])
  printMaze(maze, pacmanState)

  possibleActions = getPossibleActions(maze, pacmanState)
  nextPosition = possibleActions[0]

print('deadend')
