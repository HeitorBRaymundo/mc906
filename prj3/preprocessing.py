from scipy import fftpack
from scipy.interpolate import interp1d
import numpy as np
from scipy.signal import savgol_filter
from sklearn.base import BaseEstimator, TransformerMixin

class InterpolateRawData(BaseEstimator, TransformerMixin):

    def __init__(self, features_name=["ACC", "GYR"],
                 num_samples=50, kind='linear'):
        super().__init__()
        self.features_name = features_name
        self.num_samples = num_samples
        self.kind = kind

    def fit(self, datalist, y=None):
        return self

    def transform(self, datalist, y=None):
        X = []
        for data in datalist:
            readings = interpolate_reading(data, self.num_samples, self.kind)
            x = []
            for feature in self.features_name:
                x.extend(readings[feature][:, 1:].flatten())
            X.append(np.array(x))

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
            #X.append(np.abs(np.array(x).real))
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


def interpolate_reading(data, num_samples=50, kind='linear'):
    interpolated_readings = {}

    min_timestamp = data.get_min_timestamp()
    max_timestamp = data.get_max_timestamp()

    for key, sensor_reading in data.readings.items():

        xnew = np.linspace(min_timestamp, max_timestamp, num_samples)
        interpolated_readings[key] = [xnew]

        for component in sensor_reading[:, 1:].transpose():

            f = interp1d(sensor_reading[:, 0], component, kind=kind, fill_value="extrapolate")
            ynew = f(xnew)
            interpolated_readings[key].append(ynew)

        interpolated_readings[key] = np.array(interpolated_readings[key]).transpose()

    return interpolated_readings
