import matplotlib.pyplot as plt

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

def animate(*images, delay):
    raise NotImplementedError()

def plot_evolution_graph(*metrics):
    raise NotImplementedError()