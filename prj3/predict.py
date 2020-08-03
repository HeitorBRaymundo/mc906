import pickle

from enumerations import Author, Device, Spell
from main import convert_data
from utils import print_local_ip
from flask import Flask, request, jsonify

app = Flask(__name__)

PORT = 5555


@app.route('/collect', methods=['POST'])
def predict():
    content = request.json["data"]
    data = convert_data(content, Author.UNKNOWN, Device.UNKNOWN, Spell.UNKNOWN)

    with open('models/best_fully_connected.pkl', 'rb') as fid:
        clf = pickle.load(fid)

    result = clf.predict([data])[0]
    print(result)
    return jsonify(results=result, success=True)


if __name__ == '__main__':
    print_local_ip()
    app.run(host='0.0.0.0', port=PORT, debug=True)
