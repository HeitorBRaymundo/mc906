import pandas as pd
import matplotlib.pyplot as plt

def plot_reading(readings, title=None, ax=None):
    df = pd.DataFrame(data=readings[:, 1:], index=readings[:, 0])
    df.plot(title=title, ax=ax)


def plot_all_readings(readings_dict, keys=None, table_format=(0, 2), figsize=(15, 15)):
    if keys is None:
        keys = readings_dict.keys()

    max_lines = table_format[0] if table_format[0] != 0 else len(keys)
    max_columns = table_format[1] if table_format[1] != 0 else len(keys)

    fig = plt.figure(figsize=figsize)
    for i, key in enumerate(keys):
        ax = fig.add_subplot(max_lines, max_columns, i + 1)
        plot_reading(readings_dict[key], key, ax)

    plt.show()