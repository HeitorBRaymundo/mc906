import sys
import time

# Print the entire maze giving a matrix
def printMaze(maze, pacmanState):
  for line in maze:
    print(''.join(line))
  print('\n')
  print(pacmanState)
  print('\n')



# Giving the pacman's current position and the next position, update the maze layout.
# We update the current position to a blank space 
# and the next position we update with the Pacman indicator
def updatePacmanPosition(maze, pacmanState, nextPosition):

  currI, currJ = pacmanState['iPosition'], pacmanState['jPosition']
  maze[currI][currJ] = ' '

  [nextI, nextJ] = nextPosition

  if (maze[nextI][nextJ] == '.'):
    pacmanState['currPoints'] += 1;

  pacmanState['iPosition'] = nextI
  pacmanState['jPosition'] = nextJ
  maze[nextI][nextJ] = 'p'
  pacmanState['currSteps'] += 1;

  time.sleep(1)


# Main function to be executed, take the input from stdin and build the maze matrix
def buildMaze():
  maze = []

  maze_line = []
  for line in sys.stdin:
    for c in line:
      if (c != '\n'):
        maze_line.append(c)
    maze.append(maze_line)
    maze_line = []

  maze[1][0] = 'p'

  return maze