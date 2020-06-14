import random
import numpy as np

import genetic_algorithm
from genetic_algorithm import exp_genetic_algorithm
from puzzle import Puzzle
import math

#%%

genetic_algorithm.END = "\n"



exp_genetic_algorithm('imgs/star-wars.jpg', (5, 5),
                      pop_size=5, max_iterations=10000, mutation='swap_pieces',  crossover='random_split', mutation_swap_method="smart")

#puzzle = Puzzle('imgs/triforce.png', 3, 4)
#ps1 = ProposedSolution(puzzle.gen_shuffle_pieces())
#ps1.pieces[:,:2] = ps1.pieces[:,2:]
#plot_image(ps1.get_image_grid(), ps1.get_image(), figsize=(7, 7))

#ps1.correct_solution()

#plot_image(ps1.get_image_grid(), ps1.get_image(), figsize=(7, 7))

