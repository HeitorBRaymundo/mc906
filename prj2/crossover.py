import random
import numpy as np

from proposed_solution import ProposedSolution

def crossover1(parent1, parent2):
    raise NotImplementedError()

def crossover2(parent1, parent2):
    def getBestRow(pieces):
        bestRow = 0
        bestRowValue = 980988080808088098098

        for row in range(0, len(pieces)):
            rowValuation = 0

            for col in range(0, len(pieces[row])):
                cell = pieces[row][col]
                up = pieces[row - 1][col] if row > 0 else None
                down = pieces[row + 1][col] if row < len(pieces) - 1 else None
                left = pieces[row][col - 1] if col > 0 else None
                right = pieces[row][col + 1] if col < len(pieces[row]) - 1 else None

                cellEvaluation = cell.eval_relative(up, right, down, left)
                rowValuation += cellEvaluation

            if (rowValuation < bestRowValue):
                bestRow = row
                bestRowValue = rowValuation

        return (bestRow, bestRowValue)

    [parent1BestRow, parent1BestRowValue] = getBestRow(parent1.pieces)
    [parent2BestRow, parent2BestRowValue] = getBestRow(parent2.pieces)

    parent1Fitness = parent1.fitness_relative()
    parent2Fitness = parent2.fitness_relative()
    bestParent = parent1 if parent1Fitness < parent2Fitness else parent2

    sameRow = parent1BestRow == parent2BestRow
    if (sameRow):
        # Quando a melhor linha dos dois pais forem a mesma, vamos escolher a melhor entre elas
        selectedRow = parent1.pieces[parent1BestRow] \
            if parent1BestRowValue < parent2BestRowValue \
            else parent2.pieces[parent2BestRow]

        # O filho terá a maior parte do cromossomo sendo do melhor pai
        child = bestParent

        child.pieces[parent1BestRow] = selectedRow

        # child = handleWithRepeatedCells(child, bestParent, parent1BestRow, selectedRow)

        return child
    else:
        # O filho terá a maior parte do cromossomo sendo do melhor pai
        child = bestParent

        # Adicionamos em 2 linhas do filho, as melhores linhas de cada um dos pais
        child.pieces[parent1BestRow] = parent1.pieces[parent1BestRow]
        # child = handleWithRepeatedCells(child, bestParent, parent1BestRow, self.pieces[parent1BestRow])

        child.pieces[parent2BestRow] = parent2.pieces[parent2BestRow]
        # child = handleWithRepeatedCells(child, bestParent, parent2BestRow, other_proposed_solution.pieces[parent2BestRow])

        return child


def crossover3(parent1, parent2):
    pieces_child1 = np.empty_like(parent1.pieces)
    pieces_child2 = np.empty_like(parent2.pieces)

    if random.randint(0, 1):

        agg_sum_parent1 = [0]
        for i, fitness in enumerate(parent1.fitness_row):
            agg_sum_parent1.append(agg_sum_parent1[i - 1] + fitness)

        agg_sum_parent2 = [0]
        for i, fitness in enumerate(parent2.fitness_row[::-1]):
            agg_sum_parent2.append(agg_sum_parent2[i - 1] + fitness)

        split_point = np.argmin(list(map(np.add, agg_sum_parent1, agg_sum_parent2))[1:])

        pieces_child1[:split_point, :] = parent1.pieces[:split_point, :]
        pieces_child1[split_point:, :] = parent2.pieces[split_point:, :]

        pieces_child2[:split_point, :] = parent2.pieces[:split_point, :]
        pieces_child2[split_point:, :] = parent1.pieces[split_point:, :]

    else:

        agg_sum_parent1 = [0]
        for i, fitness in enumerate(parent1.fitness_column):
            agg_sum_parent1.append(agg_sum_parent1[i - 1] + fitness)

        agg_sum_parent2 = [0]
        for i, fitness in enumerate(parent2.fitness_column[::-1]):
            agg_sum_parent2.append(agg_sum_parent2[i - 1] + fitness)

        split_point = np.argmin(list(map(np.add, agg_sum_parent1, agg_sum_parent2))[1:])

        pieces_child1[:, :split_point] = parent1.pieces[:, :split_point]
        pieces_child1[:, split_point:] = parent2.pieces[:, split_point:]

        pieces_child2[:, :split_point] = parent2.pieces[:, :split_point]
        pieces_child2[:, split_point:] = parent1.pieces[:, split_point:]

    return ProposedSolution(pieces_child1), ProposedSolution(pieces_child2)
