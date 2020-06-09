from genetic_algorithm import ProposedSolution, exp_genetic_algorithm
from utils import plot_image
from puzzle import Puzzle
from utils import plot_image
from experiments import experiments

puzzle = Puzzle('imgs/star-wars.jpg', 3, 3)

exp_genetic_algorithm(puzzle, 10, max_iterations=10, crossover='crossover2')


# puzzle = Puzzle('imgs/triforce.png', 3, 4)
# print(puzzle.get_avg_rand_iterations())
# exp_genetic_algorithm(puzzle, 1000, max_iterations=100, crossover='crossover2')


# for exp in experiments:
#     puzzle = Puzzle(exp.puzzle_image, exp.puzzle_vertical_size, exp.puzzle_horizontal_size)
#     exp_genetic_algorithm(puzzle, exp.pop_size, max_iterations=exp.max_iterations, crossover=exp.crossover, report_time=exp.report_time)