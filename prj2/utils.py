import time

import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numpy as np

from IPython.core.display import display, HTML



def plot_image(*images, titles=[], table_format=(1, 0), figsize=(15, 15), axis=False, fontsize=20):
    '''
    Função auxiliar para comparar diferentes soluções (por imagens)
    '''
    max_lines = table_format[0] if table_format[0] != 0 else len(images)
    max_columns = table_format[1] if table_format[1] != 0 else len(images)

    fig = plt.figure(figsize=figsize)
    for i, image in enumerate(images):
        ax = fig.add_subplot(max_lines, max_columns, i + 1)

        if len(titles) == len(images):
            ax.set_xlabel(titles[i], fontsize=fontsize)

        if axis is False:
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
        ax.imshow(image)
    plt.show()


class Animation:
    def __init__(self):
        self.frames = []
        self.labels = []
        self.fig = None
        self.ax = None
        self.im = None

    def _animate(self, i):
        self.ax.set_xlabel(self.labels[i], fontsize=24)
        self.im.set_array(self.frames[i])
        return [self.im]

    def append_new_frame(self, new_frame, label):
        if len(self.frames) == 0 or not (self.frames[-1] == new_frame).all():
            self.frames.append(new_frame)
            self.labels.append(label)

    def _duplicate_last_frames(self):
        self.frames.extend([self.frames[-1]] * 10)
        self.labels.extend([self.labels[-1]] * 10)

    def _remove_last_frames(self):
        self.frames = self.frames[:-10]
        self.labels = self.labels[:-10]

    def show_video(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.xaxis.set_ticks_position('none')
        self.ax.yaxis.set_ticks_position('none')
        self.ax.set_xlabel('teste {}'.format(0))
        self.im = self.ax.imshow(self.frames[0], interpolation='none')
        self._duplicate_last_frames()
        anim = animation.FuncAnimation(self.fig, self._animate, frames=len(self.frames), interval=500, blit=True)
        plt.close()
        display(HTML(anim.to_html5_video()))
        self._remove_last_frames()



class Timer:

    def __init__(self, time_passed=None):
        self._start = None
        self.time_passed = time_passed
        self.start()

    def start(self):
        self._start = time.time()

    def get_past(self):
        return time.time() - self._start

    def check(self):
        if self.time_passed is not None and(time.time() - self._start) > self.time_passed:
            self.start()
            return True
        return False
