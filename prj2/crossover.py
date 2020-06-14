import random

import numpy as np

from proposed_solution import ProposedSolution


def crossover_best_piece_fitness(parent1, parent2):
    fitness_flatten1 = parent1.fitness_matrix.flatten()
    fitness_flatten2 = parent2.fitness_matrix.flatten()

    pieces_child = np.array([piece1 if fitness_flatten1[i] < fitness_flatten2[i] else piece2
                             for i, (piece1, piece2) in
                             enumerate(zip(parent1.pieces.flatten(), parent2.pieces.flatten()))])

    return [ProposedSolution(pieces_child.reshape(parent1.pieces.shape))]


def crossover_random_split(parent1, parent2):
    pieces_child1 = np.empty_like(parent1.pieces)
    pieces_child2 = np.empty_like(parent2.pieces)

    if random.randint(0, 1):
        split_point = random.randint(1, parent1.pieces.shape[0] - 1)
        pieces_child1[:split_point, :] = parent1.pieces[:split_point, :]
        pieces_child1[split_point:, :] = parent2.pieces[split_point:, :]
        pieces_child2[:split_point, :] = parent2.pieces[:split_point, :]
        pieces_child2[split_point:, :] = parent1.pieces[split_point:, :]
    else:
        split_point = random.randint(1, parent1.pieces.shape[1] - 1)
        pieces_child1[:, :split_point] = parent1.pieces[:, :split_point]
        pieces_child1[:, split_point:] = parent2.pieces[:, split_point:]
        pieces_child2[:, :split_point] = parent2.pieces[:, :split_point]
        pieces_child2[:, split_point:] = parent1.pieces[:, split_point:]

    return [ProposedSolution(pieces_child1), ProposedSolution(pieces_child2)]


def crossover_max_random_split(parent1, parent2):
    pieces_child1 = np.empty_like(parent1.pieces)
    pieces_child2 = np.empty_like(parent2.pieces)

    def __search_agg_fitness(agg_fitness, drawn_value):
        for i in range(1, len(agg_fitness)):
            if (agg_fitness[i] >= drawn_value):
                return i

    if random.randint(0, 1):
        aggregated_fitness = np.cumsum(np.max(parent1.fitness_matrix, axis=1))
        drawn_value = random.randint(aggregated_fitness[0], aggregated_fitness[-1]-1)
        split_point = __search_agg_fitness(aggregated_fitness, drawn_value)
        pieces_child1[:split_point, :] = parent1.pieces[:split_point, :]
        pieces_child1[split_point:, :] = parent2.pieces[split_point:, :]
        pieces_child2[:split_point, :] = parent2.pieces[:split_point, :]
        pieces_child2[split_point:, :] = parent1.pieces[split_point:, :]
    else:
        aggregated_fitness = np.cumsum(np.max(parent1.fitness_matrix, axis=0))
        drawn_value = random.randint(aggregated_fitness[0], aggregated_fitness[-1]-1)
        split_point = __search_agg_fitness(aggregated_fitness, drawn_value)
        pieces_child1[:, :split_point] = parent1.pieces[:, :split_point]
        pieces_child1[:, split_point:] = parent2.pieces[:, split_point:]
        pieces_child2[:, :split_point] = parent2.pieces[:, :split_point]
        pieces_child2[:, split_point:] = parent1.pieces[:, split_point:]

    return [ProposedSolution(pieces_child1), ProposedSolution(pieces_child2)]


def crossover_best_row(parent1, parent2):
    parent1_best_row = np.argmin(parent1.fitness_row)
    parent2_best_row = np.argmin(parent2.fitness_row)
    best_parent = parent1 if parent1.fitness < parent2.fitness else parent2

    # O filho terá a maior parte do cromossomo sendo do melhor pai
    pieces_child = np.copy(best_parent.pieces)

    if parent1_best_row == parent2_best_row:
        # Quando a melhor linha dos dois pais forem a mesma, vamos escolher a melhor entre elas
        selected_row = parent1.pieces[parent1_best_row] \
            if parent1.fitness_row[parent1_best_row] < parent2.fitness_row[parent2_best_row] \
            else parent2.pieces[parent2_best_row]

        pieces_child[parent1_best_row] = selected_row

        return [ProposedSolution(pieces_child)]
    else:
        # Adicionamos em 2 linhas do filho, as melhores linhas de cada um dos pais
        pieces_child[parent1_best_row] = parent1.pieces[parent1_best_row]
        pieces_child[parent2_best_row] = parent2.pieces[parent2_best_row]

        return [ProposedSolution(pieces_child)]


def crossover_alternate_pieces(parent1, parent2):
    pieces_child1 = np.empty_like(parent1.pieces)
    pieces_child2 = np.empty_like(parent2.pieces)

    for row in range(0, len(parent1.pieces)):
        for col in range(0, len(parent1.pieces[row])):
            if row % 2 == 0 and col % 2 != 0:
                pieces_child1[row][col] = parent1.pieces[row][col]
                pieces_child2[row][col] = parent2.pieces[row][col]
            else:
                pieces_child1[row][col] = parent2.pieces[row][col]
                pieces_child2[row][col] = parent1.pieces[row][col]

    return ProposedSolution(pieces_child1), ProposedSolution(pieces_child2)


"""
def crossover_best_split(parent1, parent2):
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
"""
