import pandas as pd

def plot_reading(readings, title=None):
    df = pd.DataFrame(data=readings[:, 1:], index=readings[:, 0])
    df.plot(title=title)


def plot_all_readings(readings_dict, keys = None):
    if keys is None:
        keys = readings_dict.keys()

    for key in keys:
        plot_reading(readings_dict[key], key)