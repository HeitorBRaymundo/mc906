class Config():
    def __init__(self, pop_size=1000, mutation_rate=10, max_iterations=10, fitness='relative', selection='roulette', mutation='mutation1', replace='elitism', crossover='crossover1', report_time=3, puzzle_image='imgs/triforce.png', puzzle_vertical_size=4, puzzle_horizontal_size=5):
        self.pop_size = 1000
        self.mutation_rate = mutation_rate
        self.max_iterations = max_iterations
        self.fitness = fitness
        self.selection = selection
        self. mutation = mutation_rate
        self.replace = replace
        self.crossover = crossover
        self.report_time = report_time
        self.puzzle_image = puzzle_image
        self.puzzle_vertical_size = puzzle_vertical_size
        self.puzzle_horizontal_size = puzzle_horizontal_size