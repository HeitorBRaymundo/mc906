import os
import pickle
from datetime import datetime
from pathlib import Path

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


class Database:

    def __init__(self, datalist):
        self.datalist = datalist

    def to_dict(self):
        return [data.__dict__ for data in self.datalist]

    def get_datalist(self):
        return self.datalist

    def get_y(self):
        return [data.spell.value for data in self.datalist]

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
