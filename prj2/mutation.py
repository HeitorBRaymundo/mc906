

"""
Generative
Destructive
Swap
Sequence swap
Flip
"""


def mutation_A (puzzle):

  print (puzzle.pieces)

  oldPiece = puzzle.pieces[2][3]
  newPiece = puzzle.pieces[0][0]
  puzzle.pieces[2][3] = newPiece
  puzzle.pieces[0][0] = oldPiece

  return puzzle


def mutation_B (self, puzzle):
  return puzzle 
  