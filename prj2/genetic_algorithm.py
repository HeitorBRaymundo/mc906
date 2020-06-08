import random
import time

from proposed_solution import ProposedSolution

from selection import roulette_selection, tournament_selection
from crossover import crossover1, crossover2, crossover3
from mutation import mutation1, mutation2
from replacement import elitism, steady_state
from utils import plot_image, Timer
from custom_statistics import Statistics


def exp_genetic_algorithm(puzzle, pop_size, mutation_rate=10, max_iterations=10, fitness='relative',
                          selection='roulette', mutation='mutation1', replace='replace_elitism',
                          crossover='crossover1', report_time=3):
    ga = GeneticAlgorithm(puzzle=puzzle, size=pop_size, mutation_rate=mutation_rate, fitness=fitness,
                          selection=selection, crossover=crossover, mutation=mutation, replace=replace)

    timer = Timer(report_time)
    # plota melhor individuo
    while ga.iterations < max_iterations and not ga.stop_criteria():
        # print(len(ga.population))
        ga.iterate()
        if timer.check():
            ga.statistics.print()

        #

    plot_image(ga.get_best().get_image_grid(), figsize=(7, 7))

    ga.statistics.print()
    print(ga)


class GeneticAlgorithm:

    def __init__(self, puzzle, size, mutation_rate, fitness, selection, crossover, mutation, replace):
        self.puzzle = puzzle
        self.population = []
        self.mutation_rate = mutation_rate
        self.fitness = fitness
        self.selection = selection
        self.replace = replace
        self.mutation = mutation
        self.crossover = crossover
        self.size = size
        self.statistics = Statistics()
        self.selection_count = round(size / 2)
        self.replacement_rate = 0.1
        self.pieces_set = set(puzzle.pieces.flatten())

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
        for indv in population:
            checkRate = random.randint(0, 100)
            if checkRate <= self.mutation_rate:
                getattr(self, '_{}'.format(self.mutation))(indv)
        return population

    def _mutation1(self, indv):
        mutation1(indv)

    def _mutation2(self, indv):
        mutation2(indv)

    def _crossover(self, parent1, parent2):
        '''
        faz crossover entre duas proposed solutions
        '''
        return getattr(self, '_{}'.format(self.crossover))(parent1, parent2)

    def _crossover1(self, parent1, parent2):
        return crossover1(parent1, parent2)

    def _crossover2(self, parent1, parent2):
        return crossover2(parent1, parent2)

    def _crossover3(self, parent1, parent2):
        child1, child2 = crossover3(parent1, parent2)
        self.puzzle.correct_solution(child1)
        self.puzzle.correct_solution(child2)
        return child1, child2

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

        # crossover entre dois individuos
        next_gen = []
        for i in range(1, len(selected_parents), 2):
            parent1 = selected_parents[i - 1]
            parent2 = selected_parents[i]
            child1, child2 = self._crossover(parent1, parent2)
            next_gen.extend([child1, child2])

            # child1 = self._crossover(parent1, parent2)
            # next_gen.extend([child1])

        self._complete_next_gen_with_clones(next_gen)

        next_gen = self._mutation(next_gen)
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
