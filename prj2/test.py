import crossover
import mutation
from genetic_algorithm import ProposedSolution, exp_genetic_algorithm
from utils import plot_image
from puzzle import Puzzle
import random
import numpy as np
from config import Config


puzzle = Puzzle('imgs/triforce.png', 3, 4)
ps1 = ProposedSolution(puzzle.pieces)
ps2 = ProposedSolution(puzzle.gen_shuffle_pieces())

plot_image(ps2.get_image())

plot_image(crossover.crossover_best_row(ps1, ps2)[0].get_image())
