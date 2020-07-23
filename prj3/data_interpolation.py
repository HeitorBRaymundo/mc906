from scipy.interpolate import interp1d
import numpy as np


def _get_min_timestamp(readings):
    first_timestamp_list = []
    for key in readings.keys():
        first_timestamp_list.append(readings[key][0][0])
    return min(first_timestamp_list)

def _get_max_timestamp(readings):
    last_timestamp_list = []
    for key in readings.keys():
        last_timestamp_list.append(readings[key][-1][0])
    return max(last_timestamp_list)

def interpolate_readings(readings, num_samples=50):

    interpolated_readings = {}

    min_timestamp = _get_min_timestamp(readings)
    max_timestamp = _get_max_timestamp(readings)

    for key, sensor_reading in readings.items():

        xnew = np.linspace(min_timestamp, max_timestamp, num_samples)
        interpolated_readings[key] = [xnew]

        for component in sensor_reading[:, 1:].transpose():
            f = interp1d(sensor_reading[:, 0], component, fill_value="extrapolate")
            ynew = f(xnew)
            interpolated_readings[key].append(ynew)

        interpolated_readings[key] = np.array(interpolated_readings[key]).transpose()

    return interpolated_readings