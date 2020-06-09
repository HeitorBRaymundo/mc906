import random
import numpy as np

from proposed_solution import ProposedSolution

def crossover1(parent1, parent2):
    raise NotImplementedError()

def crossover2(parent1, parent2):

    def getBestRow(ps):
        
        bestRow = 0
        for row in range(0 , len(ps.fitness_row)):
            if (ps.fitness_row[row] <= ps.fitness_row[bestRow]):
                bestRow = row

        return bestRow

    parent1BestRow = getBestRow(parent1)
    parent2BestRow = getBestRow(parent2)

    parent1Fitness = parent1.fitness_relative()
    parent2Fitness = parent2.fitness_relative()
    bestParent = parent1 if parent1Fitness < parent2Fitness else parent2

    # O filho terá a maior parte do cromossomo sendo do melhor pai
    pieces_child1 = np.empty_like(bestParent.pieces)

    sameRow = parent1BestRow == parent2BestRow
    if (sameRow):
        # Quando a melhor linha dos dois pais forem a mesma, vamos escolher a melhor entre elas
        selectedRow = parent1.pieces[parent1BestRow] \
            if parent1.fitness_row[parent1BestRow] < parent2.fitness_row[parent2BestRow] \
            else parent2.pieces[parent2BestRow]

        pieces_child1[parent1BestRow] = selectedRow

        for row in range(0, len(pieces_child1)):
            if (row == parent1BestRow):
                continue
            pieces_child1[row] = bestParent.pieces[row]

        return ProposedSolution(pieces_child1)
    else:
        # Adicionamos em 2 linhas do filho, as melhores linhas de cada um dos pais
        pieces_child1[parent1BestRow] = parent1.pieces[parent1BestRow]
        pieces_child1[parent2BestRow] = parent2.pieces[parent2BestRow]

        for row in range(0, len(pieces_child1)):
            if (row == parent1BestRow or row == parent2BestRow):
                continue
            pieces_child1[row] = bestParent.pieces[row]

        return ProposedSolution(pieces_child1)

def crossover21(parent1, parent2):
    pieces_child1 = np.empty_like(parent1.pieces)
    pieces_child2 = np.empty_like(parent2.pieces)

    for row in range(0, len(parent1.pieces)):
        for col in range(0, len(parent1.pieces[row])):
            parent1Up = parent1.pieces[row - 1][col] if row - 1 >= 0 else None
            parent1Right = parent1.pieces[row][col + 1] if col + 1 < len(parent1.pieces[row]) - 1 else None
            parent1Down = parent1.pieces[row + 1][col] if row + 1 < len(parent1.pieces) - 1 else None
            parent1Left = parent1.pieces[row][col - 1] if col - 1 >= 0 else None
            
            evaluatedParent1Piece = parent1.pieces[row][col].eval_relative(parent1Up, parent1Right, parent1Down, parent1Left)

            parent2Up = parent2.pieces[row - 1][col] if row - 1 >= 0 else None
            parent2Right = parent2.pieces[row][col + 1] if col + 1 < len(parent1.pieces[row]) - 1 else None
            parent2Down = parent2.pieces[row + 1][col] if row + 1 < len(parent1.pieces) - 1 else None
            parent2Left = parent2.pieces[row][col - 1] if col - 1 >= 0 else None
            
            evaluatedParent2Piece = parent2.pieces[row][col].eval_relative(parent2Up, parent2Right, parent2Down, parent2Left)

            if (evaluatedParent1Piece < evaluatedParent2Piece):
                pieces_child1[row][col] = parent1.pieces[row][col]
                pieces_child2[row][col] = parent1.pieces[row][col]
            else:
                pieces_child1[row][col] = parent2.pieces[row][col]
                pieces_child2[row][col] = parent2.pieces[row][col]

    return ProposedSolution(pieces_child1), ProposedSolution(pieces_child2)


def crossover22(parent1, parent2):
    pieces_child1 = np.empty_like(parent1.pieces)
    pieces_child2 = np.empty_like(parent2.pieces)

    for row in range(0, len(parent1.pieces)):
        for col in range(0, len(parent1.pieces[row])):
            if (row % 2 == 0 and col % 2 != 0):
               pieces_child1[row][col] = parent1.pieces[row][col]
               pieces_child2[row][col] = parent2.pieces[row][col]
            else:
               pieces_child1[row][col] = parent2.pieces[row][col]
               pieces_child2[row][col] = parent1.pieces[row][col]

    return ProposedSolution(pieces_child1), ProposedSolution(pieces_child2)

def crossover3(parent1, parent2):
    pieces_child1 = np.empty_like(parent1.pieces)
    pieces_child2 = np.empty_like(parent2.pieces)

    if random.randint(0, 1):


        """
        agg_sum_parent1 = [0]
        for i, fitness in enumerate(parent1.fitness_row):
            agg_sum_parent1.append(agg_sum_parent1[i - 1] + fitness)

        agg_sum_parent2 = [0]
        for i, fitness in enumerate(parent2.fitness_row[::-1]):
            agg_sum_parent2.append(agg_sum_parent2[i - 1] + fitness)
        
        split_point = np.argmin(list(map(np.add, agg_sum_parent1, agg_sum_parent2))[1:])
        """

        split_point = random.randint(1, parent1.pieces.shape[0]-1)

        pieces_child1[:split_point, :] = parent1.pieces[:split_point, :]
        pieces_child1[split_point:, :] = parent2.pieces[split_point:, :]

        pieces_child2[:split_point, :] = parent2.pieces[:split_point, :]
        pieces_child2[split_point:, :] = parent1.pieces[split_point:, :]

        #print(split_point)

    else:

        """
        agg_sum_parent1 = [0]
        for i, fitness in enumerate(parent1.fitness_column):
            agg_sum_parent1.append(agg_sum_parent1[i - 1] + fitness)

        agg_sum_parent2 = [0]
        for i, fitness in enumerate(parent2.fitness_column[::-1]):
            agg_sum_parent2.append(agg_sum_parent2[i - 1] + fitness)
            
        split_point = np.argmin(list(map(np.add, agg_sum_parent1, agg_sum_parent2))[1:])
        """
        split_point = random.randint(1, parent1.pieces.shape[1]-1)

        pieces_child1[:, :split_point] = parent1.pieces[:, :split_point]
        pieces_child1[:, split_point:] = parent2.pieces[:, split_point:]

        pieces_child2[:, :split_point] = parent2.pieces[:, :split_point]
        pieces_child2[:, split_point:] = parent1.pieces[:, split_point:]

        #print(split_point)


    return ProposedSolution(pieces_child1), ProposedSolution(pieces_child2)
