import matplotlib.pyplot as plt
import statistics

class Statistics():
    def __init__(self):
        self.min = []
        self.max = []
        self.media = []

    def update(self, population):
        self.min.append(min(population))
        self.max.append(max(population))
        #self.media.append(statistics.mean(population))

    def print(self):
        self.print_min()
        self.print_max()
        self.print_media()

    def print_min(self):
        plt.plot(list(map(lambda x: x.fitness, self.min)))
        plt.ylabel('min')
        plt.show()

    def print_max(self):
        plt.plot(list(map(lambda x: x.fitness, self.max)))
        plt.ylabel('max')
        plt.show()

    def print_media(self):
        plt.plot(self.media)
        plt.ylabel('media')
        plt.show()