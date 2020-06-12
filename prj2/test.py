import crossover
import mutation
from genetic_algorithm import ProposedSolution, exp_genetic_algorithm
from selection import roulette_selection
from utils import plot_image
from puzzle import Puzzle
import random
import numpy as np
from config import Config


puzzle = Puzzle('imgs/triforce.png', 2, 2)
ps1 = ProposedSolution(puzzle.gen_shuffle_pieces())

plot_image(ps1.get_image())
ps1.fitness_relative()
print(ps1.fitness_matrix)

mutation.mutation_swap_pieces(ps1)

ps1.fitness_relative()
print(ps1.fitness_matrix)

plot_image(ps1.get_image())



