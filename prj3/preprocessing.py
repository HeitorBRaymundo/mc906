from scipy.interpolate import interp1d
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class InterpolateRawData(BaseEstimator, TransformerMixin):

    def __init__(self, features_name=["ACC", "GYR"],
                 num_samples=50, method='interp1d'):
        super().__init__()
        self.features_name = features_name
        self.num_samples = num_samples
        self.method = method

    def fit(self, datalist, y=None):
        return self

    def transform(self, datalist, y=None):
        X = []
        for data in datalist:
            readings = interpolate_reading(data, self.num_samples, self.method)

            x = []
            for feature in self.features_name:
                x.extend(readings[feature][1:].flatten())
            X.append(np.array(x))

        return X

def interpolate_reading(data, num_samples=50, method='interp1d'):
    interpolated_readings = {}

    min_timestamp = data.get_min_timestamp()
    max_timestamp = data.get_max_timestamp()

    for key, sensor_reading in data.readings.items():

        xnew = np.linspace(min_timestamp, max_timestamp, num_samples)
        interpolated_readings[key] = [xnew]

        for component in sensor_reading[:, 1:].transpose():

            if method == 'interp1d':
                f = interp1d(sensor_reading[:, 0], component, fill_value="extrapolate")
            else:
                raise Exception('Método {} não reconhecido.'.format(method))

            ynew = f(xnew)
            interpolated_readings[key].append(ynew)

        interpolated_readings[key] = np.array(interpolated_readings[key]).transpose()

    return interpolated_readings
