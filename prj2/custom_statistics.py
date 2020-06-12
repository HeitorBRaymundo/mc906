import matplotlib.pyplot as plt
import numpy as np


class Statistics:

    def __init__(self):
        self.min = []
        self.max = []
        self.media = []

    def update(self, population):
        self.min.append(min(population))
        self.max.append(max(population))
        self.media.append(np.mean([ps.fitness for ps in population]))

    def plot(self):
        plt.figure(figsize=(10, 7))
        x_axis = range(0, len(self.min))
        self.plot_min(x_axis)
        self.plot_max(x_axis)
        self.plot_media(x_axis)
        plt.xlabel('Iterações', fontsize=14)
        plt.ylabel('Fitness', fontsize=14)
        plt.legend()
        plt.show()

    def plot_min(self, x_axis):
        plt.plot(x_axis, list(map(lambda x: x.fitness, self.min)), label='min')

    def plot_max(self, x_axis):
        plt.plot(x_axis, list(map(lambda x: x.fitness, self.max)), label='max')

    def plot_media(self, x_axis):
        plt.plot(x_axis, self.media, label='media')

    def get_last(self):
        return "{} - {} - {} (min - media - max)".format(self.min[-1], self.media[-1], self.max[-1])
