import matplotlib.pyplot as plt
import numpy as np

class Statistics():
    def __init__(self):
        self.min = []
        self.max = []
        self.media = []

    def update(self, population):
        self.min.append(min(population))
        self.max.append(max(population))
        self.media.append(np.mean([ps.fitness for ps in population]))

    def print(self):
        x_axis = range(0, len(self.min))
        self.print_min(x_axis)
        self.print_max(x_axis)
        self.print_media(x_axis)
        plt.xlabel('Iterações')
        plt.ylabel('Metricas')
        plt.legend()
        plt.show()

    def print_min(self, x_axis):
        plt.plot(x_axis, list(map(lambda x: x.fitness, self.min)), label = 'min')

    def print_max(self, x_axis):
        plt.plot(x_axis, list(map(lambda x: x.fitness, self.max)), label = 'max')

    def print_media(self, x_axis):
        plt.plot(x_axis, self.media, label = 'media')