from piece import PiecesManager
import numpy as np

from utils import plot_image


def exp_genetic_algorithm(puzzle, pop_size, mutation_rate=10, max_iterations=10, fitness='relative',
                          selection='selection1', mutation='mutation1', replace='replace1', crossover='crossover1'):

    ga = GeneticAlgorithm(puzzle=puzzle, size=pop_size, mutation_rate=mutation_rate, fitness=fitness,
                          selection=selection, crossover=crossover, mutation=mutation, replace=replace)

    # plota melhor individuo
    plot_image(ga.get_best().get_image_grid(), figsize=(7, 7))
    while ga.iterations < max_iterations and not ga.stop_criteria():
        #ga.iterate()
        plot_image(ga.get_best().get_image_grid(), figsize=(7, 7))

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
        self.statistics = []


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
        return getattr(self, '_{}'.format(self.selection))()

    def _selection1(self):
        raise NotImplementedError()

    def _selection2(self):
        raise NotImplementedError()

    def _replace(self):
        '''
        retorna proxima geracao
        '''
        return getattr(self, '_{}'.format(self.replace))()

    def _replace1(self, new_population):
        raise NotImplementedError()

    def _replace2(self, new_population):
        raise NotImplementedError()

    def _mutation(self, population):
        '''
        faz mutacao considerando self.mutation_rate
        '''
        # chamar metodo de mutação selecionado por self.mutation:
        # getattr(self,'_{}'.format(self.mutation))(population)
        raise NotImplementedError()

    def _crossover(self, parent1, parent2):
        '''
        faz crossover entre duas proposed solutions
        '''
        return getattr(parent1, self.crossover)(parent2)

    def _update_statistics(self):
        '''
        salva min, max e media... em self.statistics para plotar acompanhamento
        '''
        raise NotImplementedError()

    def iterate(self):

        # seleciona candidatos a pais (ordenados)
        selected_parents = self._selection()

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
        self.population = self._replace()

        self._update_statistics()
        self.iterations = self.iterations + self.iterations

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

    def mutation1(self):
        raise NotImplementedError()

    def mutation2(self):
        raise NotImplementedError()

    def crossover1(self, other_proposed_solution):
        raise NotImplementedError()

    def crossover2(self, other_proposed_solution):
        raise NotImplementedError()

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