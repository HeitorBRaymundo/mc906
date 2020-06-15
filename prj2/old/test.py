import crossover
from genetic_algorithm import ProposedSolution
from utils import plot_image
from puzzle import Puzzle
import numpy as np

"""
puzzle = Puzzle('imgs/triforce.png', 2, 2)
ps1 = ProposedSolution(puzzle.gen_shuffle_pieces())
ps2 = ProposedSolution(puzzle.gen_shuffle_pieces())

child = crossover.crossover_random_split(ps1, ps2)[0]

plot_image(child.get_image())
puzzle.correct_solution(child)
plot_image(child.get_image())

"""

puzzle = Puzzle('../imgs/star-wars.jpg', 3, 4)

ps1 = ProposedSolution(np.copy(puzzle.pieces))
copy = ps1.pieces[0][0]
ps1.pieces[0][0] = ps1.pieces[1][1]
ps1.pieces[1][1] = copy
ps1.fitness_relative()




ps2 = ProposedSolution(np.copy(puzzle.pieces))
copy = ps2.pieces[2][2]
ps2.pieces[2][2] = ps2.pieces[1][2]
ps2.pieces[1][2] = copy

ps2.fitness_relative()

plot_image(ps1.get_image(), ps2.get_image())
childs = crossover.crossover_max_random_split(ps1, ps2)
plot_image(childs[0].get_image(), childs[1].get_image())




