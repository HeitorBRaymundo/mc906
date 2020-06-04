from random import *
import numpy as np


def roulette_selection(population, selection_count):
    if len(population) == 0 or selection_count == 0:
        return []

    aggragated_fitness = []
    curr_agg_fitness = 0.0

    for proposed_solution in population:
        curr_agg_fitness += 1.0 / (proposed_solution.fitness + 1.0)
        aggragated_fitness.append(curr_agg_fitness)

    result_population = []
    for i in range(0, selection_count):
        drawn_value = uniform(0, curr_agg_fitness)
        piece_index = __search_agg_fitness(aggragated_fitness, drawn_value)
        result_population.append(population[piece_index])

    return result_population


def tournament_selection(population, selection_count):
    if len(population) == 0 or selection_count == 0:
        return []

    tournament_size = round(len(population) / 10)
    result_population = []

    for i in range(0, selection_count):
        tournament_participants = __choose_tournament_participants(population, tournament_size)
        tournament_winner = __perform_tournament(tournament_participants)
        result_population.append(tournament_winner)

    return result_population


# roulette selection utility functions
def __search_agg_fitness(agg_fitness, drawn_value):
    for i in range(0, len(agg_fitness)):
        if (agg_fitness[i] >= drawn_value):
            return i


# tournament selection utility functions
def __choose_tournament_participants(population, tournament_size):
    participants = []
    for i in range(0, tournament_size):
        cur_participant_index = randrange(0, len(population))
        participants.append(population[cur_participant_index])

    return participants


def __perform_tournament(tournament_participants):
    best_fitness = np.inf
    best_participant = None

    for participant in tournament_participants:
        if participant.fitness < best_fitness:
            best_participant = participant
            best_fitness = participant.fitness

    return best_participant
