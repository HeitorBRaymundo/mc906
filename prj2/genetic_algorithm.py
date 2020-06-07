from piece import PiecesManager
import numpy as np
import random
import math
from copy import deepcopy

from selection import roulette_selection, tournament_selection
from replacement import elitism, steady_state
from utils import plot_image
from custom_statistics import Statistics

def exp_genetic_algorithm(puzzle, pop_size, mutation_rate=10, max_iterations=10, fitness='relative',
                          selection='roulette', mutation='mutation1', replace='replace_elitism', crossover='crossover1'):

    ga = GeneticAlgorithm(puzzle=puzzle, size=pop_size, mutation_rate=mutation_rate, fitness=fitness,
                          selection=selection, crossover=crossover, mutation=mutation, replace=replace)

    # plota melhor individuo
    plot_image(ga.get_best().get_image_grid(), figsize=(7, 7))
    while ga.iterations < max_iterations and not ga.stop_criteria():
        ga.iterate()
        plot_image(ga.get_best().get_image_grid(), figsize=(7, 7))

    ga.statistics.print()
    print(ga)


class GeneticAlgorithm:

    def __init__(self, puzzle, size, mutation_rate, fitness, selection, crossover, mutation, replace):
        self.population = []
        self.mutation_rate = mutation_rate
        self.fitness = fitness
        self.selection = selection
        self.replace = replace
        self.mutation = mutation
        self.crossover = crossover
        self.size = size
        self.statistics = Statistics()
        self.selection_count = round(size/2)
        self.replacement_rate = 0.1


        # inicializa populacao de forma randomica
        for i in range(size):
            ps = ProposedSolution(puzzle.gen_shuffle_pieces())
            self.population.append(ps)

        # computa o valor de fitness para cada objeto dentro de population
        self._eval_fitness(self.population)

        self.population.sort()
        self.iterations = 0


    def _eval_fitness(self, population):
        # chama o metodo fitness_absolute ou fitness_relative de cada individuo
        for ps in population:
            getattr(ps, 'fitness_{}'.format(self.fitness))()

    def sort_population(self):
        self.population.sort()

    def get_best(self):
        return min(self.population)

    def stop_criteria(self):
        return self.get_best().fitness == 0

    def _selection(self):
        '''
        retorna lista dos pais para reproducao
        '''
        return getattr(self, '_selection_{}'.format(self.selection))()

    def _selection_roulette(self):
        return roulette_selection(self.population, self.selection_count)

    def _selection_tournament(self):
        return tournament_selection(self.population, self.selection_count)

    def _replace(self, next_gen):
        '''
        retorna proxima geracao
        '''
        return getattr(self, '_{}'.format(self.replace))(next_gen)

    def _replace_elitism(self, new_population):
        return elitism(self.get_best(), new_population)

    def _replace_steady_state(self, new_population):
        return steady_state(self.population, new_population, steady_rate=self.replacement_rate)

    def _mutation(self, population):
        '''
        faz mutacao considerando self.mutation_rate
        '''
        # chamar metodo de mutação selecionado por self.mutation:
        checkRate = random.randint(0, 100)
        if (checkRate <= self.mutation_rate):
            return getattr(self,'_{}'.format(self.mutation))(population)

    def _crossover(self, parent1, parent2):
        '''
        faz crossover entre duas proposed solutions
        '''
        return getattr(parent1, self.crossover)(parent2)

    def _update_statistics(self):
        '''
        salva min, max e media... em self.statistics para plotar acompanhamento
        '''
        self.statistics.update(self.population)

    def iterate(self):

        # seleciona candidatos a pais (ordenados)
        selected_parents = self._selection()

        print('passou aqui')

        # crossover entre dois individuos
        next_gen = []
        for i in range(1, len(selected_parents), 2):
            parent1 = selected_parents[i-1]
            parent2 = selected_parents[i]
            child1, child2 = self._crossover(parent1, parent2)
            next_gen.extend([child1, child2])

        # avalia fitness e ordena next_gen
        self._eval_fitness(next_gen)
        next_gen.sort()

        # substitui pela proxima geracao
        self.population = self._replace(next_gen)

        self._update_statistics()
        self.iterations += 1

    def __str__(self):
        string = ""
        for ps in self.population:
            string = string + str(ps.fitness) + " "
        return string


class ProposedSolution(PiecesManager):
    # chromosome

    def __init__(self, pieces):
        super().__init__(pieces)
        self.fitness = np.inf
        self.pieces_set = set(self.pieces.flatten())

    def mutation1(self):
        # Swap sequence: swapping lines
        swapFromRow = random.randint(0, len(self.pieces) - 1)
        swapToRow = random.randint(0, len(self.pieces) - 1)

        while (swapFromRow == swapToRow):
            swapToRow = random.randint(0, len(self.pieces) - 1)

        fromRow = deepcopy(self.pieces[swapFromRow])
        toRow = deepcopy(self.pieces[swapToRow])
        self.pieces[swapToRow] = fromRow
        self.pieces[swapFromRow] = toRow

    def mutation2(self):
        # Swap: swapping n cells, where n is a number calculated giving the size of the puzzle and a random rate
        rows = len(self.pieces)
        cols = len(self.pieces[0])

        swapRate = random.randint(10, 30)/100
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

            fromCel = self.pieces[randFromRow][randFromCol]
            toCel = self.pieces[randToRow][randToCol]

            self.pieces[randToRow][randToCol] = fromCel
            self.pieces[randFromRow][randFromCol] = toCel

    def crossover1(self, other_proposed_solution):
        raise NotImplementedError()

    def crossover2(self, other_proposed_solution):
        raise NotImplementedError()

    def correct_solution(self):
        remaining_set = self.pieces_set - set(self.pieces.flatten())
        track_set = set()

        new_pieces = []
        for piece in self.pieces.flatten():
            if piece not in track_set:
                new_pieces.append(piece)
            else:
                new_pieces.append(remaining_set.pop())
            track_set.add(piece)

        self.pieces = np.array(new_pieces).reshape(self.pieces.shape)


    def fitness_absolute(self):
        """
        Conta o numero de peças na posição incorreta
        """
        result = 0
        for i in range(self.pieces.shape[0]):
            for j in range(self.pieces.shape[1]):
                result = result + 1 - self.pieces[i][j].eval_absolute(j, i)

        self.fitness = result
        return result

    def fitness_relative(self):
        """
        Conta o numero total de vizinhos errados
        """
        result = 0
        for i in range(self.pieces.shape[0]):
            for j in range(self.pieces.shape[1]):
                up = self.get_piece(i - 1, j)
                right = self.get_piece(i, j + 1)
                down = self.get_piece(i + 1, j)
                left = self.get_piece(i, j - 1)
                result = result + 4 - self.pieces[i][j].eval_relative(up, right, down, left)

        self.fitness = result
        return result

    def __eq__(self, other):
        return self.fitness == other.fitness and self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness
