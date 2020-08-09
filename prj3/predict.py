import csv
import pickle
from collections import defaultdict

import numpy as np

from data import Data
from enumerations import Author, Device, Spell
from main import convert_data
from utils import print_address
from flask import Flask, request, jsonify

app = Flask(__name__)

PORT = 5555

with open('models/best_random_forest.pkl', 'rb') as fid:
    clf = pickle.load(fid)

with open('models/best_random_forest_acc.pkl', 'rb') as fid:
    clf_acc = pickle.load(fid)


def convert_data(content, spell, author, device):
    readings = defaultdict(list)

    for data_list in list(csv.reader(content.splitlines(), skipinitialspace=True)):
        read = [float(data_list[1])]
        read.extend([float(data) for data in data_list[2:]])
        readings[data_list[0]].append(read)

    first_timestamp_list = []
    for key in readings.keys():
        readings[key] = np.array(readings[key])
        if len(readings[key]) > 1:
            readings[key] = readings[key][np.argsort(readings[key][:, 0])]
            first_timestamp_list.append(readings[key][0][0])

    first_timestamp = min(first_timestamp_list)
    for key in readings.keys():
        for read in readings[key]:
            read[0] = read[0] - first_timestamp

    return Data(readings, spell, author, device)

@app.route('/collect', methods=['POST'])
def predict():
    content = request.json["data"]
    data = convert_data(content, Author.UNKNOWN, Device.UNKNOWN, Spell.UNKNOWN)

    if "GYR" not in list(data.readings.keys()):
        result = clf_acc.predict([data])[0]
    else:
        result = clf.predict([data])[0]

    print(result)
    return jsonify(results=result, success=True)


if __name__ == '__main__':
    print_address(PORT)
    app.run(host='0.0.0.0', port=PORT, debug=True)
