import random
from copy import copy


def mutation1(ps):
    # Swap sequence: swapping lines
    swapFromRow = random.randint(0, len(ps.pieces) - 1)
    swapToRow = random.randint(0, len(ps.pieces) - 1)

    while (swapFromRow == swapToRow):
        swapToRow = random.randint(0, len(ps.pieces) - 1)

    fromRow = copy(ps.pieces[swapFromRow])
    toRow = copy(ps.pieces[swapToRow])

    ps.pieces[swapToRow] = fromRow
    ps.pieces[swapFromRow] = toRow

def mutation2(ps):
    # Swap: swapping n cells, where n is a number calculated giving the size of the puzzle and a random rate
    rows = len(ps.pieces)
    cols = len(ps.pieces[0])

    swapRate = random.randint(10, 30) / 100
    base = rows * cols
    numberOfSwaps = int(base * swapRate)

    for i in range(0, numberOfSwaps):
        randFromRow = random.randint(0, rows - 1)
        randFromCol = random.randint(0, cols - 1)

        randToRow = random.randint(0, rows - 1)
        randToCol = random.randint(0, cols - 1)

        while (randFromCol == randToCol and randFromRow == randToRow):
            randToRow = random.randint(0, rows - 1)
            randToCol = random.randint(0, cols - 1)

        fromCel = ps.pieces[randFromRow][randFromCol]
        toCel = ps.pieces[randToRow][randToCol]

        ps.pieces[randToRow][randToCol] = fromCel
        ps.pieces[randFromRow][randFromCol] = toCel