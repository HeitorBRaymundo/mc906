from piece import PiecesManager
import numpy as np
import random
import math
from copy import deepcopy

from selection import roulette_selection, tournament_selection
from replacement import elitism, steady_state
from crossover import crossover_simplified_sholomon
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

    #ga.statistics.print()
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
        rows = len(self.pieces)
        cols = len(self.pieces[0])
        child_pieces = crossover_simplified_sholomon(self.pieces, other_proposed_solution.pieces, rows, cols)
        child = ProposedSolution(child_pieces)
        child.correct_solution()
        return child

    def crossover2(self, other_proposed_solution):

        [parent1BestRow, parent1BestRowValue] = getBestRow(self.pieces)
        [parent2BestRow, parent2BestRowValue] = getBestRow(other_proposed_solution.pieces)

        print('Parent 1 best row:', parent1BestRow, 'Parent 2 best row:', parent2BestRow)

        parent1Fitness = self.fitness_relative()
        parent2Fitness = other_proposed_solution.fitness_relative()
        bestParent = self if parent1Fitness < parent2Fitness else other_proposed_solution


        print('Fitness pai 1: ', parent1Fitness)
        print('Fitness pai 2: ', parent2Fitness)

        sameRow = parent1BestRow == parent2BestRow
        if (sameRow):
            # Quando a melhor linha dos dois pais forem a mesma, vamos escolher a melhor entre elas
            selectedRow = deepcopy(self.pieces[parent1BestRow]) \
                if parent1BestRowValue < parent2BestRowValue \
                else deepcopy(other_proposed_solution.pieces[parent2BestRow])

            # O filho terá a maior parte do cromossomo sendo do melhor pai
            child = deepcopy(bestParent)
            
            child = handleWithRepeatedCells(child, bestParent, parent1BestRow, selectedRow)
            # repeatedCells = []
            # for cell in selectedRow:
            #     for row in range(0, len(bestParent.pieces)):
            #         if (row == parent1BestRow):
            #             continue;
            #         for col in range(0, len(bestParent.pieces[row])):
            #             if (bestParent.pieces[row][col].pos == cell.pos):
            #                 dict = {}
            #                 dict['cell'] = cell
            #                 dict['position'] = (row, col)
            #                 repeatedCells.append(dict)

            #         # repeatedCellsInRow = list(filter(lambda checkCell: checkCell.pos == cell.pos, bestParent.pieces[row]))
            #         # repeatedCells.extend(repeatedCellsInRow)

            # # print('Melhor linha: ', list(map(lambda x: x.pos, selectedRow)))
            # # print('Linha a ser substituída do melhor pai: ', list(map(lambda x: x.pos, bestParent.pieces[parent1BestRow])))
            # # print(list(map(lambda x: x['position'], repeatedCells)))
            # # print('Peças repetidas: ', list(map(lambda x: x['cell'].pos, repeatedCells)))

            # bestParent.pieces[parent1BestRow]
            # piecesToReplace = []
            # for cell in bestParent.pieces[parent1BestRow]:

            #     includeOnReplacement = True

            #     for replacementCell in selectedRow:
            #         if (replacementCell.pos == cell.pos):
            #             includeOnReplacement = False
            #             break
                
            #     if (includeOnReplacement):
            #         piecesToReplace.append(cell)

            # # print('Peças a serem recolocadas: ', list(map(lambda x: x.pos, piecesToReplace)))

            # # Adicionamos ao filho a melhor linha entre os dois pais
            # child.pieces[parent1BestRow] = selectedRow

            # for repeatedCell in range(0, len(repeatedCells)):
            #     [row, col] = repeatedCells[repeatedCell]['position']
            #     child.pieces[row][col] = deepcopy(piecesToReplace[repeatedCell])

            print('Fitness filho: ', child.fitness_relative())

            # print('Pai 1')
            # for row in self.pieces:
            #     print(list(map(lambda x: x.pos, row)))

            # print('Pai 2')
            # for row in other_proposed_solution.pieces:
            #     print(list(map(lambda x: x.pos, row)))

            # print('Filho')
            # for row in child.pieces:
            #     print(list(map(lambda x: x.pos, row)))


            return child
        else:
            # O filho terá a maior parte do cromossomo sendo do melhor pai
            child = deepcopy(bestParent)

            # Adicionamos em 2 linhas do filho, as melhores linhas de cada um dos pais
            child.pieces[parent1BestRow] = deepcopy(self.pieces[parent1BestRow])
            child = handleWithRepeatedCells(child, bestParent, parent1BestRow, self.pieces[parent1BestRow])

            child.pieces[parent2BestRow] = deepcopy(other_proposed_solution.pieces[parent2BestRow])
            child = handleWithRepeatedCells(child, bestParent, parent2BestRow, other_proposed_solution.pieces[parent2BestRow])
            
            print('Fitness filho: ', child.fitness_relative())
            return child
       

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


def getBestRow (pieces):
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


def handleWithRepeatedCells (child, parent, changedRow, selectedRow):
    repeatedCells = []
    for cell in selectedRow:
        for row in range(0, len(parent.pieces)):
            if (row == changedRow):
                continue;
            for col in range(0, len(parent.pieces[row])):
                if (parent.pieces[row][col].pos == cell.pos):
                    dict = {}
                    dict['cell'] = cell
                    dict['position'] = (row, col)
                    repeatedCells.append(dict)

    parent.pieces[changedRow]
    piecesToReplace = []
    for cell in parent.pieces[changedRow]:

        includeOnReplacement = True

        for replacementCell in selectedRow:
            if (replacementCell.pos == cell.pos):
                includeOnReplacement = False
                break
        
        if (includeOnReplacement):
            piecesToReplace.append(cell)

    # Adicionamos ao filho a melhor linha entre os dois pais
    child.pieces[changedRow] = selectedRow

    for repeatedCell in range(0, len(repeatedCells)):
        [row, col] = repeatedCells[repeatedCell]['position']
        child.pieces[row][col] = deepcopy(piecesToReplace[repeatedCell])

    return deepcopy(child)