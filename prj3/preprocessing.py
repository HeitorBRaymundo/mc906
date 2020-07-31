from scipy import fftpack
from scipy.interpolate import interp1d
import numpy as np
from scipy.signal import savgol_filter
from sklearn.base import BaseEstimator, TransformerMixin


class InterpolateRawData(BaseEstimator, TransformerMixin):

    def __init__(self, features_name=["ACC", "GYR"],
                 num_samples=50, max_time=6000, timestep=10, flatten_data=True, kind='linear'):
        super().__init__()
        self.features_name = features_name
        self.num_samples = num_samples
        self.flatten_data = flatten_data
        self.max_time = max_time
        self.timestep = timestep
        self.kind = kind

    def fit(self, datalist, y=None):
        return self

    def transform(self, datalist, y=None):

        max_data = int(self.max_time / self.timestep)

        def pad(x):
            if len(x) > max_data:
                x = x[:max_data]
            else:
                x = np.pad(x, (0, max_data - len(x)), 'constant', constant_values=(0, 0))
            return x

        X = []
        for data in datalist:
            readings = interpolate_reading(data, self.num_samples, self.timestep, self.kind)
            x_list = []
            for feature in self.features_name:
                if self.flatten_data:
                    if self.num_samples is None:
                        for read in readings[feature][:, 1:].transpose():
                            x_list.extend(pad(read))
                    else:
                        x_list.extend(readings[feature][:, 1:].transpose().flatten())
                else:
                    for read in readings[feature][:, 1:].transpose():
                        if self.num_samples is None:
                            x_list.append(pad(read))
                        else:
                            x_list.append(read)


            if self.flatten_data:
                X.append(np.array(x_list))
            else:
                X.append(np.array(x_list).transpose())

        return np.array(X)


class FastFourierTransform(BaseEstimator, TransformerMixin):

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
            readings = fast_fourier_transform(data, self.num_samples)

            x = []
            for feature in self.features_name:
                x.extend(readings[feature][:, 1:].flatten().real)
                x.extend(readings[feature][:, 1:].flatten().imag)
            # X.append(np.abs(np.array(x).real))
            X.append(np.array(x))

        return np.array(X)


class SavGolTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, polyorder=3, window_length=5, deriv=0, range=None):
        self.polyorder = polyorder
        self.window_length = window_length
        self.deriv = deriv
        self.range = range

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        range = self.range
        if self.range is None:
            range = (0, X.shape[1])

        X_sav = savgol_filter(X[:, range[0]:range[1]], self.window_length, self.polyorder, self.deriv, axis=1)

        return np.c_[X[:, :range[0]], X_sav, X[:, range[1]:]]


def fast_fourier_transform(data, num_samples=50):
    interpolated_readings = interpolate_reading(data, 50000, kind='cubic')
    fourier_readings = {}

    for key, sensor_reading in interpolated_readings.items():

        freq = np.fft.fftfreq(50000, d=sensor_reading[1][0] - sensor_reading[0][0])

        filter = np.where(np.logical_and(freq > 0, freq <= 0.1))
        xnew = np.linspace(0, 0.0075, num_samples)
        fourier_readings[key] = [xnew]

        for component in sensor_reading[:, 1:].transpose():
            yf = fftpack.fft(component)
            f = interp1d(freq[filter], yf[filter], fill_value="extrapolate")
            fourier_readings[key].append(f(xnew))
        fourier_readings[key] = np.array(fourier_readings[key]).transpose()
    return fourier_readings


def interpolate_reading(data, num_samples=50, timestep=None, kind='linear'):
    interpolated_readings = {}

    min_timestamp = data.get_min_timestamp()
    max_timestamp = data.get_max_timestamp()

    for key, sensor_reading in data.readings.items():

        if num_samples is not None:
            xnew = np.linspace(min_timestamp, max_timestamp, num_samples)
        else:
            xnew = np.arange(min_timestamp, max_timestamp, timestep)

        interpolated_readings[key] = [xnew]

        for component in sensor_reading[:, 1:].transpose():
            f = interp1d(sensor_reading[:, 0], component, kind=kind, fill_value="extrapolate")
            ynew = f(xnew)
            interpolated_readings[key].append(ynew)

        interpolated_readings[key] = np.array(interpolated_readings[key]).transpose()

    return interpolated_readings
