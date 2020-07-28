import csv
from collections import defaultdict

from data import Data
from enumerations import Author, Device, Spell
from utils import print_local_ip
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

PORT = 5555

def convert_data(content, spell, author, device):
    readings = {
        "ACC": [], "GYR": []
    }

    for data_list in list(csv.reader(content.splitlines(), skipinitialspace=True)):
        read = [float(data_list[1])]
        read.extend([float(data) for data in data_list[2:]])
        readings[data_list[0]].append(read)

    first_timestamp_list = []
    for key in readings.keys():
        if len(readings[key]) < 2:
            return
        readings[key] = np.array(readings[key])
        readings[key] = readings[key][np.argsort(readings[key][:, 0])]
        first_timestamp_list.append(readings[key][0][0])

    first_timestamp = min(first_timestamp_list)
    for key in readings.keys():
        for read in readings[key]:
            read[0] = read[0] - first_timestamp

    return Data(readings, spell, author, device)


@app.route('/collect', methods=['POST'])
def collect():
    AUTHOR = Author.GUILHERME
    DEVICE = Device.SAMSUNG_S8
    SPELL = Spell.REVELIO

    content = request.json["data"]

    data = convert_data(content, SPELL, AUTHOR, DEVICE)

    if data is not None:

        print("Foram capurados {} dados, aproximados {:.2f} ms. ".format(data.get_len(),
                                                                         data.get_max_timestamp() -
                                                                         data.get_min_timestamp()))
        file_path = data.save()
        print("Dados salvos em {}. ".format(file_path))

    else:
        print("Dados faltantes...")

    return jsonify(success=True)


@app.route('/predict', methods=['POST'])
def predict():
    # TODO: colocar melhor modelo para previsão
    content = request.json["data"]
    data = convert_data(content, Author.UNKNOWN, Device.UNKNOWN, Spell.UNKNOWN)

    if data is not None:
        # PREDICT
        pass

    return jsonify(success=True)


if __name__ == '__main__':
    print_local_ip()
    app.run(host='0.0.0.0', port=PORT, debug=True)

