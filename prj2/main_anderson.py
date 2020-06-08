
from genetic_algorithm import exp_genetic_algorithm
from puzzle import Puzzle
import math

#%%

#puzzle = Puzzle('imgs/triforce.png', 5, 5)
puzzle = Puzzle('imgs/triforce.png', 3, 4)

print(puzzle.get_avg_rand_iterations())
exp_genetic_algorithm(puzzle, 1000, max_iterations=1000, crossover='crossover3')




#puzzle = Puzzle('imgs/triforce.png', 3, 4)
#ps1 = ProposedSolution(puzzle.gen_shuffle_pieces())
#ps1.pieces[:,:2] = ps1.pieces[:,2:]
#plot_image(ps1.get_image_grid(), ps1.get_image(), figsize=(7, 7))

#ps1.correct_solution()

#plot_image(ps1.get_image_grid(), ps1.get_image(), figsize=(7, 7))

