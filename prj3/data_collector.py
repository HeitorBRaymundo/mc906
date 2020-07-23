import csv

from data import Data
from enumerations import Author, Device, Spell
from utils import print_local_ip
from flask import Flask, request, jsonify
import numpy as np

AUTHOR = Author.ANDERSON
DEVICE = Device.SAMSUNG_A5
SPELL = Spell.ALOHOMORA
PORT = 5555

print_local_ip()

app = Flask(__name__)


@app.route('/collect', methods=['POST'])
def collect():
    content = request.json["data"]

    readings = {
        "ACC": [],
        "GYR": [],
        "MAG": [],
        "GRA": [],
        "LAC": [],
        "RTV": [],
        "RTM": [],
        "ORI": []
    }


    for data_list in list(csv.reader(content.splitlines(), skipinitialspace=True)):
        read = [float(data_list[1])]
        read.extend([float(data) for data in data_list[2:]])
        readings[data_list[0]].append(read)

    data_len = 0

    first_timestamp_list = []
    for key in readings.keys():
        readings[key] = np.array(readings[key])
        if len(readings[key]) > 1:
            readings[key] = readings[key][np.argsort(readings[key][:, 0])]
        data_len = data_len + len(readings[key])
        first_timestamp_list.append(readings[key][0][0])

    first_timestamp = min(first_timestamp_list)
    for key in readings.keys():
        for read in readings[key]:
            read[0] = read[0] - first_timestamp

    data = Data(readings, SPELL, AUTHOR, DEVICE)

    print("Foram capurados {} dados, aproximados {:.2f} ms. ".format(data_len,
                                                                           readings["ACC"][-1][0] - readings["ACC"][0][
                                                                               0]))
    file_path = data.save()
    print("Dados salvos em {}. ".format(file_path))

    resp = jsonify(success=True)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
