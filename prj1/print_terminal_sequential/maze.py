import sys
import time
from actions import getPossibleActions


# Print the entire maze giving a matrix
def printMaze(maze, pacmanState):
  for line in maze:
    print(''.join(line))
  print('\n')
  print(pacmanState)
  print(getPossibleActions(maze, pacmanState))
  print('\n')



# Giving the pacman's state and the next position, update the maze layout.
# We update the current position of pacman to a blank space 
# and the next position we update with the Pacman indicator ('p')
def updatePacmanPosition(maze, pacmanState, nextPosition):

  currI, currJ = pacmanState['iPosition'], pacmanState['jPosition']
  maze[currI][currJ] = ' '

  [nextI, nextJ] = nextPosition
  if (maze[nextI][nextJ] == '.'):
    pacmanState['currPoints'] += 1

  pacmanState['iPosition'] = nextI
  pacmanState['jPosition'] = nextJ
  maze[nextI][nextJ] = 'p'
  pacmanState['currSteps'] += 1

  time.sleep(1)


# Main function to be executed, take the input from stdin and build the maze matrix
def buildMaze(pacmanState):
  maze = []

  initialI, initialJ = pacmanState['iPosition'], pacmanState['jPosition']

  maze_line = []
  for line in sys.stdin:
    for c in line:
      if (c != '\n'):
        maze_line.append(c)
    maze.append(maze_line)
    maze_line = []

  maze[initialI][initialJ] = 'p'

  return maze