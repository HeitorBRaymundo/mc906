import random

from proposed_solution import ProposedSolution
from puzzle import Puzzle

from selection import roulette_selection, tournament_selection
from crossover import crossover_best_piece_fitness, crossover_random_split, crossover_best_row, \
    crossover_alternate_pieces, crossover_max_random_split
from mutation import mutation_swap_pieces, mutation_swap_lines_columns, mutation_split_change_swap_pieces
from replacement import elitism, steady_state, extermination
from utils import plot_image, Timer, Animation
from custom_statistics import Statistics
import numpy as np

END = ""

def exp_genetic_algorithm(puzzle_file, puzzle_splits, pop_size, selection='roulette',
                          crossover='random_split', mutation='swap_pieces', replace='elitism', selection_count=None,
                          selection_tournament_size=None, crossover_rate=100, mutation_rate=10,
                          mutation_swapness=(10, 30), mutation_swap_method="standard", replacement_rate=0.1,
                          max_iterations=10, report_time=1):
    np.random.seed(42)
    random.seed(42)

    puzzle = Puzzle(puzzle_file, puzzle_splits[0], puzzle_splits[1])

    ga = GeneticAlgorithm(puzzle=puzzle, size=pop_size, selection=selection, crossover=crossover,
                          mutation=mutation, replace=replace, selection_count=selection_count,
                          selection_tournament_size=selection_tournament_size, mutation_rate=mutation_rate,
                          crossover_rate=crossover_rate, mutation_swapness=mutation_swapness,
                          mutation_swap_method=mutation_swap_method, replacement_rate=replacement_rate)

    print("Número de combinações possíveis: {}".format(puzzle.get_avg_rand_iterations()))

    timer = Timer(report_time)
    timer_algorithm = Timer()
    animation = Animation()

    while ga.iterations < max_iterations and not ga.stop_criteria():
        ga.iterate()
        if timer.check():
            print('Iteração atual {}: {}\r'.format(ga.iterations, ga.statistics.get_last()), end=END)
        animation.append_new_frame(ga.get_best().get_image(), "Melhor indivíduo iteração {}".format(ga.iterations))

    print()
    print("Tempo de execução: {}s".format(timer_algorithm.get_past()))
    plot_image(ga.get_best().get_image_grid(), figsize=(16, 9), titles=["Melhor indivíduo final"], fontsize=24)
    ga.statistics.plot()
    print("Generating video... ")
    animation.show_video()
    print("Finished")


class GeneticAlgorithm:

    def __init__(self, puzzle, size, selection, crossover, mutation, replace,
                 selection_count, selection_tournament_size, crossover_rate, mutation_rate,
                 mutation_swapness, mutation_swap_method, replacement_rate):

        self.puzzle = puzzle
        self.population = []
        self.size = size
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.replace = replace
        if selection_count is None:
            self.selection_count = round(size / 2)
        else:
            self.selection_count = selection_count
        if selection_tournament_size is None:
            self.selection_tournament_size = round(size / 2)
        else:
            self.selection_tournament_size = selection_tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.mutation_swapness = mutation_swapness
        self.mutation_swap_method = mutation_swap_method
        self.replacement_rate = replacement_rate

        self.statistics = Statistics()
        self.pieces_set = set(puzzle.pieces.flatten())

        # inicializa populacao de forma randomica
        self.population = [ProposedSolution(puzzle.gen_shuffle_pieces()) for _ in range(size)]

        # computa o valor de fitness para cada objeto dentro de population
        self._eval_fitness(self.population)
        self.sort_population()
        self.iterations = 0

    def _eval_fitness(self, population):
        # chama o metodo fitness_absolute ou fitness_relative de cada individuo
        for ps in population:
            ps.fitness_relative()

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
        return tournament_selection(self.population, self.selection_count, self.selection_tournament_size)

    def _crossover(self, selected_parents):
        '''
        faz crossover nos selected_parents
        '''

        next_gen = []
        for i in range(1, len(selected_parents), 2):
            check_rate = random.randint(0, 100)
            if check_rate <= self.mutation_rate:
                parent1 = selected_parents[i - 1]
                parent2 = selected_parents[i]
                child_list = getattr(self, '_crossover_{}'.format(self.crossover))(parent1, parent2)
                next_gen.extend(child_list)

        return next_gen

    def _crossover_best_piece_fitness(self, parent1, parent2):
        child_list = crossover_best_piece_fitness(parent1, parent2)
        for child in child_list:
            self.puzzle.correct_solution(child)
        return child_list

    def _crossover_random_split(self, parent1, parent2):
        child_list = crossover_random_split(parent1, parent2)
        for child in child_list:
            self.puzzle.correct_solution(child)
        return child_list

    def _crossover_max_random_split(self, parent1, parent2):
        child_list = crossover_max_random_split(parent1, parent2)
        for child in child_list:
            self.puzzle.correct_solution(child)
        return child_list

    def _crossover_best_row(self, parent1, parent2):
        child_list = crossover_best_row(parent1, parent2)
        for child in child_list:
            self.puzzle.correct_solution(child)
        return child_list

    def _crossover_alternate_pieces(self, parent1, parent2):
        child_list = crossover_alternate_pieces(parent1, parent2)
        for child in child_list:
            self.puzzle.correct_solution(child)
        return child_list

    def _mutation(self, population):
        '''
        faz mutacao considerando self.mutation_rate
        '''
        # chamar metodo de mutação selecionado por self.mutation:
        for proposed_solution in population:
            check_rate = random.randint(0, 100)
            if check_rate <= self.mutation_rate:
                getattr(self, '_mutation_{}'.format(self.mutation))(proposed_solution)
        return population

    def _mutation_swap_pieces(self, proposed_solution):
        mutation_swap_pieces(proposed_solution, self.mutation_swapness, self.mutation_swap_method)

    def _mutation_swap_lines_columns(self, proposed_solution):
        mutation_swap_lines_columns(proposed_solution)

    def _mutation_split_change_swap_pieces(self, proposed_solution):
        mutation_split_change_swap_pieces(proposed_solution, self.mutation_swapness, self.mutation_swap_method)

    def _replace(self, next_gen):
        '''
        retorna proxima geracao
        '''
        return getattr(self, '_replace_{}'.format(self.replace))(next_gen)[:self.size]

    def _replace_elitism(self, new_population):
        return elitism(self.get_best(), new_population)

    def _replace_steady_state(self, new_population):
        return steady_state(self.population, new_population, steady_rate=self.replacement_rate)

    def _replace_extermination(self, new_population):
        return extermination(self.population, new_population)

    def _update_statistics(self):
        '''
        salva min, max e media... em self.statistics para plotar acompanhamento
        '''
        self.statistics.update(self.population)

    def _complete_next_gen_with_clones(self, next_gen):
        elements_to_clone = len(self.population) - len(next_gen)
        cloned_elements = self.population[:elements_to_clone]

        for i in range(len(cloned_elements)):
            cloned_elements[i] = cloned_elements[i].clone()

        next_gen.extend(cloned_elements)

    def iterate(self):
        # seleciona candidatos a pais (ordenados)
        selected_parents = self._selection()

        # crossover
        next_gen = self._crossover(selected_parents)

        self._complete_next_gen_with_clones(next_gen)

        next_gen = self._mutation(next_gen)
        # avalia fitness e ordena next_gen
        self._eval_fitness(next_gen)
        next_gen.sort()

        # substitui pela proxima geracao
        self.population = self._replace(next_gen)
        self.sort_population()

        self._update_statistics()
        self.iterations += 1
