
# Return an array of possible actions, including the name of action and the destiny position
def getPossibleActions(maze, pacmanState):

  currI, currJ = pacmanState['iPosition'], pacmanState['jPosition']

  possibleActions = []

  #Check right
  rightI, rightJ = currI, currJ + 1
  if (checkBound(rightI, rightJ)):
    rightPosition = maze[rightI][rightJ]
    if (checkObstacle(rightPosition)):
      action = {
        'action': 'RIGHT',
        'pos': [rightI, rightJ]
      }
      possibleActions.append(action)


  #Check down
  downI, downJ = currI + 1, currJ 
  if (checkBound(downI, downJ)):
    downPosition = maze[downI][downJ]
    if (checkObstacle(downPosition)):
      action = {
        'action': 'DOWN',
        'pos': [downI, downJ]
      }
      possibleActions.append(action)

  #Check left
  leftI, leftJ = currI, currJ - 1
  if (checkBound(leftI, leftJ)):
    leftPosition = maze[leftI][leftJ]
    if (checkObstacle(leftPosition)):
      action = {
        'action': 'LEFT',
        'pos': [leftI, leftJ]
      }
      possibleActions.append(action)

  #Check up
  upI, upJ = currI - 1, currJ
  if (checkBound(upI, upJ)):
    upPosition = maze[upI][upJ]
    if (checkObstacle(upPosition)):
      action = {
        'action': 'UP',
        'pos': [upI, upJ]
      }
      possibleActions.append(action)

  return possibleActions

def checkBound(i, j):
  if (i < 0 or i > 30 or j < 0 or j > 30):
    return False
  return True


def checkObstacle(position):
  if (position == '|'):
    return False
  return True