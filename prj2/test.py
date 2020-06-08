from genetic_algorithm import ProposedSolution
from puzzle import Puzzle
from utils import plot_image

puzzle = Puzzle('imgs/triforce.png', 3, 4)
ps1 = ProposedSolution(puzzle.gen_shuffle_pieces())
plot_image(ps1.get_image_grid(), ps1.get_image(), figsize=(7, 7))
print("fitness relative = {}".format(ps1.fitness_relative()))

print(ps1.fitness_column)
print(ps1.fitness_row)
print(ps1.fitness_matrix)

