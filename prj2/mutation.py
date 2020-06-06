import random
import math

"""
Generative
Destructive
Swap
Sequence swap
Flip
"""


def mutation_A ():

  matrix = [
    [1, 2, 3],
    [4, 5, 6]
  ]

  for line in matrix:
    print(line)

  swapFromLine = random.randint(0, len(matrix) - 1)
  swapToLine = random.randint(0, len(matrix) - 1)

  while (swapFromLine == swapToLine):
      swapToLine = random.randint(0, len(matrix) - 1)

  print('Values:', swapFromLine, swapToLine)

  fromLine = matrix[swapFromLine]
  toLine = matrix[swapToLine]
  matrix[swapToLine] = fromLine
  matrix[swapFromLine] = toLine

  print('New matrix')

  for line in matrix:
    print(line)

mutation_A()

def mutation_B ():
  matrix = [
      [1, 2, 3, 4, 5, 6, 7, 8, 9],
      [11, 12, 13, 14, 15, 16, 17, 18, 19],
      [21, 22, 23, 24, 25, 26, 27, 28, 29],
      [31, 32, 33, 34, 35, 36, 37, 38, 39],
      [41, 42, 43, 44, 45, 46, 47, 48, 49],
      [51, 52, 53, 54, 55, 56, 57, 58, 59],
      [61, 62, 63, 64, 65, 66, 67, 68, 69],
    ]

  for line in matrix:
    print(line)
  
  rows = len(matrix)
  cols = len(matrix[0])

  swapRate = random.randint(10, 30)/100
  base = rows * cols
  numberOfSwaps = math.floor(base * swapRate)

  print('Swap rate:', swapRate, 'Base:', base, 'N of swaps:', numberOfSwaps)

  for i in range(0, numberOfSwaps):
    randFromRow = random.randint(0, rows - 1)
    randFromCol = random.randint(0, cols - 1)

    randToRow = random.randint(0, rows - 1)
    randToCol = random.randint(0, cols - 1)

    while (randFromCol == randToCol and randFromRow == randToRow):
      randToRow = random.randint(0, rows - 1)
      randToCol = random.randint(0, cols - 1)
 

    fromCel = matrix[randFromRow][randFromCol]
    toCel = matrix[randToRow][randToCol]

    print('[', randFromRow, ',', randFromCol, '] = ', fromCel, ' <-> ', '[', randToRow, ',', randToCol, '] = ', toCel)

    matrix[randToRow][randToCol] = fromCel
    matrix[randFromRow][randFromCol] = toCel

  for line in matrix:
    print(line)

# mutation_B()
  