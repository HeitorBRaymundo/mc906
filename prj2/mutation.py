import random
import numpy as np

def mutation_swap_lines_columns(ps):
    if random.randint(0, 1):
        _mutation_swap_lines(ps)
    else:
        _mutation_swap_columns(ps)

def mutation_swap_pieces(ps, swapness=(10, 30)):
    # Swap: swapping n cells, where n is a number calculated giving the size of the puzzle and a random rate
    rows = len(ps.pieces)
    cols = len(ps.pieces[0])

    swap_rate = random.randint(swapness[0], swapness[1]) / 100
    base = rows * cols
    number_of_swaps = int(base * swap_rate)

    for i in range(0, number_of_swaps):
        rand_from_row = random.randint(0, rows - 1)
        rand_from_col = random.randint(0, cols - 1)

        rand_to_row = random.randint(0, rows - 1)
        rand_to_col = random.randint(0, cols - 1)

        while rand_from_col == rand_to_col and rand_from_row == rand_to_row:
            rand_to_row = random.randint(0, rows - 1)
            rand_to_col = random.randint(0, cols - 1)

        from_cel = ps.pieces[rand_from_row][rand_from_col]
        to_cel = ps.pieces[rand_to_row][rand_to_col]

        ps.pieces[rand_to_row][rand_to_col] = from_cel
        ps.pieces[rand_from_row][rand_from_col] = to_cel

def _mutation_swap_lines(ps):
    # Swap sequence: swapping lines
    swap_from_row = random.randint(0, ps.pieces.shape[0] - 1)
    swap_to_row = random.randint(0, ps.pieces.shape[0] - 1)

    while swap_from_row == swap_to_row:
        swap_to_row = random.randint(0, ps.pieces.shape[0] - 1)

    from_row = np.copy(ps.pieces[swap_from_row, :])
    to_row = np.copy(ps.pieces[swap_to_row, :])

    ps.pieces[swap_to_row, :] = from_row
    ps.pieces[swap_from_row, :] = to_row

def _mutation_swap_columns(ps):
    # Swap sequence: swapping lines
    swap_from_column = random.randint(0, ps.pieces.shape[1] - 1)
    swap_to_column = random.randint(0, ps.pieces.shape[1] - 1)

    while swap_from_column == swap_to_column:
        swap_to_column = random.randint(0, ps.pieces.shape[1] - 1)

    from_column = np.copy(ps.pieces[:, swap_from_column])
    to_column = np.copy(ps.pieces[:, swap_to_column])

    ps.pieces[:, swap_to_column] = from_column
    ps.pieces[:, swap_from_column] = to_column


