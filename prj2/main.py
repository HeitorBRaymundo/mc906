from genetic_algorithm import ProposedSolution, exp_genetic_algorithm
from utils import plot_image
from puzzle import Puzzle
from utils import plot_image

# puzzle = Puzzle('imgs/triforce.png', 4, 4)
# ps1 = ProposedSolution(puzzle.gen_shuffle_pieces())
# ps2 = ProposedSolution(puzzle.gen_shuffle_pieces())

#plot_image(ps1.get_image_grid(), figsize=(7, 7))
#plot_image(ps2.get_image_grid(), figsize=(7, 7))

# child = ps1.crossover2(ps2)
#plot_image(child.get_image_grid(), figsize=(7, 7))


puzzle = Puzzle('imgs/triforce.png', 3, 4)
print(puzzle.get_avg_rand_iterations())
exp_genetic_algorithm(puzzle, 1000, max_iterations=100, crossover='crossover2')
