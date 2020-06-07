import random
import numpy
from copy import deepcopy


# Simplified sholomon crossover generates a single child
def crossover_simplified_sholomon(parent1, parent2, max_rows, max_columns):

    # first selected piece is chosen randomly
    selected_row = random.randint(0, max_rows - 1)
    selected_column = random.randint(0, max_columns - 1)
    total_pieces = (max_columns * max_rows)
    child_pieces_count = 0

    # indicates wheter position has a piece or not in child
    child_map = numpy.zeros((max_rows, max_columns)) 

    child = deepcopy(parent1)

    # check if child is complete
    while child_pieces_count < total_pieces:
        # apply sholomon A phase
        new_selected_piece, selected_row, selected_column = simplified_sholomon_A_phase(parent1, parent2, selected_row, selected_column, max_rows, max_columns, child) 

        if new_selected_piece != None:
            child[selected_row][selected_column] = new_selected_piece
            child_map[selected_row][selected_column] = 1
            child_pieces_count += 1
        else:
            # if parents do not agree about any neighbor, choose one at random (phase B)
            new_selected_piece, selected_row, selected_column = simplified_sholomon_B_phase(parent1, parent2, selected_row, selected_column, max_rows, max_columns, child) 
            child[selected_row][selected_column] = new_selected_piece
            child_map[selected_row][selected_column] = 1
            child_pieces_count += 1

    return child

# the idea of phase A is to find out, for a selected piece, which neighbors both parents agree about (which neighbors are equal in parent1 and parent2)
# if there is more than one agreeded neighbor, one is returned at random
def simplified_sholomon_A_phase(parent1, parent2, selected_row, selected_column, max_rows, max_columns, child):

    agreeded_pieces = []
    agreeded_row_pos = []
    agreeded_column_pos = []

    if selected_column > 0:
        if (parent1[selected_row][selected_column - 1] == parent2[selected_row][selected_column - 1]) and child[selected_row][selected_column - 1] == 0:
            # parents agree about left neighbor of selected piece
            
            agreeded_pieces.append(parent1[selected_row][selected_column - 1])
            agreeded_row_pos.append(selected_row)
            agreeded_column_pos.append(selected_column - 1)
    if selected_row > 0:
        if (parent1[selected_row - 1][selected_column] == parent2[selected_row -1][selected_column]) and child[selected_row - 1][selected_column] == 0:
            # parents agree about top neighbor of selected piece
            
            agreeded_pieces.append(parent1[selected_row - 1][selected_column])
            agreeded_row_pos.append(selected_row - 1)
            agreeded_column_pos.append(selected_column)
    if selected_row < max_rows - 1:
        if (parent1[selected_row + 1][selected_column] == parent2[selected_row + 1][selected_column]) and child[selected_row + 1][selected_column] == 0:
            # parents agree about right neighbor of selected piece
            
            agreeded_pieces.append(parent1[selected_row + 1][selected_column])
            agreeded_row_pos.append(selected_row + 1)
            agreeded_column_pos.append(selected_column)
    if selected_column < max_columns - 1:
        if (parent1[selected_row][selected_column + 1] == parent2[selected_row][selected_column + 1]) and child[selected_row][selected_column - 1] == 0:
            # parents agree about right neighbor of selected piece
        
            agreeded_pieces.append(parent1[selected_row][selected_column + 1])
            agreeded_row_pos.append(selected_row)
            agreeded_column_pos.append(selected_column)

    agreeded_pieces_count = len(agreeded_pieces)
    if agreeded_pieces_count > 0:
        # if there is more than one agreeded piece than choose one randomly
        index = random.randint(0, agreeded_pieces_count - 1)
        return agreeded_pieces[index], agreeded_row_pos[index], agreeded_column_pos[index]
    else:    
        return None, selected_row, selected_column 

def simplified_sholomon_B_phase(parent1, parent2, selected_row, selected_column, max_rows, max_columns, child):
    
    # select either parent1 or parent2 
    random_parent = random.randint(0, 1) 
    possible_rows_pos = []
    possible_column_pos = []

    # check which neighbors exist
    if selected_row > 0:
        possible_rows_pos.append(selected_row - 1)
    if selected_row < max_rows - 1:
        possible_rows_pos.append(selected_row + 1)
    if selected_column > 0:
        possible_column_pos.append(selected_column - 1)
    if selected_column < max_columns - 1:
        possible_column_pos.append(selected_column + 1)

    possible_rows_count = len(possible_rows_pos)
    possible_column_count = len(possible_column_pos)

    random_row_index = random.randint(0, possible_rows_count - 1)
    random_column_index = random.randint(0, possible_column_count - 1)

    selected_row = possible_rows_pos[random_row_index]
    selected_column = possible_column_pos[random_column_index]

    # check if selected piece is not already filled in child 
    while child[selected_row][selected_column] == 0: 
        random_row_index = random.randint(0, possible_rows_count - 1)
        random_column_index = random.randint(0, possible_column_count - 1)
        selected_row = possible_rows_pos[random_row_index]
        selected_column = possible_column_pos[random_column_index]

    # returns a random available neighbor of selected piece
    if random_parent ==  0:
        return parent1[selected_row][selected_column], selected_row, selected_column
    else:
        return parent2[selected_row][selected_column], selected_row, selected_column
