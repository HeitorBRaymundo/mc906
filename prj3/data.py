import os
import pickle
from datetime import datetime
from pathlib import Path

ROOT_FOLDER = 'data'

def load_database():
    database = []
    for path in Path(ROOT_FOLDER).rglob('*.pkl'):
        database.append(Data.load_filepath(str(path)).__dict__)

    return database

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
        folder = os.path.join(ROOT_FOLDER, self.author.value, self.spell.value)

        if not os.path.exists(folder):
            os.makedirs(folder)

        file_path = os.path.join(folder, '{}__{}.pkl'.format(self.date, self.device.value))

        with open(file_path, 'wb') as f:
            pickle.dump([self.readings, self.spell, self.author, self.device, self.date], f)

    def __str__(self):
        return self.__dict__

