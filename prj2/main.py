from genetic_algorithm import ProposedSolution, exp_genetic_algorithm
from utils import plot_image
from puzzle import Puzzle
from mutation import mutation_A
from utils import plot_image

puzzle = Puzzle('imgs/triforce.png', 3, 4)
exp_genetic_algorithm(puzzle, 1, max_iterations=0)

newPuzzle = mutation_A(puzzle)
exp_genetic_algorithm(newPuzzle, 1, max_iterations=0)

