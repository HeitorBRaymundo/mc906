import os
import pickle
from datetime import datetime
from pathlib import Path
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.utils import shuffle

from cross_validation import cv_folds_author
from enumerations import Author, Spell

ROOT_FOLDER = 'data'


class Data:

    def __init__(self, readings, spell, author, device):
        self.readings = readings
        self.spell = spell
        self.author = author
        self.device = device
        self.date = datetime.now()

    @staticmethod
    def load_filepath(filepath):
        with open(filepath, "rb") as f:
            data_file = pickle.load(f)
        data = Data(*data_file[:-1])
        data.date = data_file[-1]

        return data

    @staticmethod
    def load(author, spell, filename):
        folder = os.path.join(ROOT_FOLDER, author.value, spell.value)
        file_path = os.path.join(folder, filename)
        return Data.load_filepath(file_path)

    def save(self):

        if self.spell == Spell.UNKNOWN:
            return

        folder = os.path.join(ROOT_FOLDER, self.author.value, self.spell.value)

        if not os.path.exists(folder):
            os.makedirs(folder)

        file_path = os.path.join(folder, '{}__{}.pkl'.format(self.date, self.device.value))

        with open(file_path, 'wb') as f:
            pickle.dump([self.readings, self.spell, self.author, self.device, self.date], f)

        return file_path

    def get_min_timestamp(self):
        first_timestamp_list = []
        for key in self.readings.keys():
            first_timestamp_list.append(self.readings[key][0][0])
        return min(first_timestamp_list)

    def get_max_timestamp(self):
        last_timestamp_list = []
        for key in self.readings.keys():
            last_timestamp_list.append(self.readings[key][-1][0])
        return max(last_timestamp_list)

    def get_len(self):
        data_len = 0
        for key in self.readings.keys():
            data_len = data_len + len(self.readings[key])
        return data_len

    def __str__(self):
        return self.__dict__

    def to_dict(self):
        return {
            'spell': self.spell.value,
            'author': self.author.value,
            'device': self.device.value,
            'date': self.date,
            'acc_data': len(self.readings['ACC']),
            'gyr_data': len(self.readings['GYR']),
            'time': self.get_max_timestamp() - self.get_min_timestamp()
        }


class Database:

    def __init__(self, datalist):
        self.datalist = shuffle(datalist, random_state=0)
        self.datadict = [data.to_dict() for data in self.datalist]
        self.X = np.array(self.datalist)
        self.y = np.array([data.spell.value for data in self.datalist])
        self.cv_author = (list(cv_folds_author(self.X)))

        self.label_encoder = LabelEncoder()
        integer_encoded = self.label_encoder.fit_transform(self.y)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        self.ones_encoder = OneHotEncoder(sparse=False)
        self.y_encoded = self.ones_encoder.fit_transform(integer_encoded)

    def decode(self, onehot_encoded):
        inverted_list = []
        for onehot_encoded_data in onehot_encoded:
            inverted_list.append(self.label_encoder.inverse_transform([np.argmax(onehot_encoded_data)]))
        return np.array(inverted_list)


def load_database():
    database = []
    for path in Path(ROOT_FOLDER).rglob('*.pkl'):
        database.append(Data.load_filepath(str(path)))
    return Database(database)


def load_database_test():
    database = []
    for path in Path(ROOT_FOLDER).rglob('*.pkl'):
        data = Data.load_filepath(str(path))
        if data.author == Author.TESTER:
            database.append(data)
    return Database(database)


def load_database_train():
    database = []
    for path in Path(ROOT_FOLDER).rglob('*.pkl'):
        data = Data.load_filepath(str(path))
        if data.author != Author.TESTER:
            database.append(data)
    return Database(database)
