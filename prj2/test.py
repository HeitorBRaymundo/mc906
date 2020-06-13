import crossover
import mutation
from genetic_algorithm import ProposedSolution, exp_genetic_algorithm
from selection import roulette_selection
from utils import plot_image
from puzzle import Puzzle
import random
import numpy as np
from config import Config


"""
puzzle = Puzzle('imgs/triforce.png', 2, 2)
ps1 = ProposedSolution(puzzle.gen_shuffle_pieces())
ps2 = ProposedSolution(puzzle.gen_shuffle_pieces())

child = crossover.crossover_random_split(ps1, ps2)[0]

plot_image(child.get_image())
puzzle.correct_solution(child)
plot_image(child.get_image())

"""

puzzle = Puzzle('imgs/star-wars.jpg', 3, 3)
ps1 = ProposedSolution(puzzle.pieces)
copy = puzzle.pieces[0][0]
puzzle.pieces[0][0] = puzzle.pieces[1][1]
puzzle.pieces[1][1] = copy
ps1.fitness_relative()
plot_image(ps1.get_image())
mutation._mutation_swap_pieces(ps1)
plot_image(ps1.get_image())




