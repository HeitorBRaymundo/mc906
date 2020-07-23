#%%


import pandas as pd
from data import load_database
from data_interpolation import interpolate_readings
from plotter import plot_all_readings
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

database = pd.DataFrame(data=load_database())
readings = database['readings'][0]

print(interpolate_readings(readings))

plot_all_readings(readings)
