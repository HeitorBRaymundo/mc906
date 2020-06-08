from config import Config

experiments = [Config(pop_size=1000, mutation_rate=10, max_iterations=10, fitness='relative', selection='roulette', mutation='mutation1', replace='elitism', crossover='crossover3', report_time=3, puzzle_image='imgs/triforce.png', puzzle_vertical_size=4, puzzle_horizontal_size=5),
               Config(pop_size=1000, mutation_rate=10, max_iterations=10, fitness='relative', selection='tournament', mutation='mutation1', replace='elitism', crossover='crossover3', report_time=3, puzzle_image='imgs/triforce.png', puzzle_vertical_size=4, puzzle_horizontal_size=5)]