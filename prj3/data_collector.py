import csv
import socket
import threading
import numpy as np
import collections
import sys
import time

PORT = 5555

class DataCollector:

    def print_progress(self):
        while 1:
            time.sleep(0.1)
            if self.recoding and len(self.recorded_messages) > 0:
                print("{}\r".format(len(self.recorded_messages)), end='')
                sys.stdout.flush()

    def worker(self):
        count = 0
        while 1:
            message, address = self.socket.recvfrom(8192)
            self.last_messages.append(message)
            count = count + 1
            if self.recoding:
                self.recorded_messages.append(message)

    def __init__(self, maxlen=1000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', PORT))
        self.recorded_messages = []
        self.recoding = False
        self.last_messages = collections.deque(maxlen=maxlen)
        self.started = False
        thread_messages = threading.Thread(target=self.worker)
        thread_messages.daemon = True
        thread_messages.start()

        thread_status = threading.Thread(target=self.print_progress)
        thread_status.daemon = True
        thread_status.start()

    @staticmethod
    def _get_read(data_list):

        def _get_data(dl, char_identity):
            for i in range(1, len(dl), 4):
                if dl[i] == char_identity:
                    return map(float, dl[i + 1:i + 4])
            return [np.nan, np.nan, np.nan]

        time = float(data_list[0])
        accelerometer = _get_data(data_list, '3')
        gyroscope = _get_data(data_list, '4')
        magnetic_field = _get_data(data_list, '5')
        orientation = _get_data(data_list, '81')
        linear_acc = _get_data(data_list, '82')
        gravity = _get_data(data_list, '83')
        rotation_vector = _get_data(data_list, '84')

        read = [time]
        read.extend(accelerometer)
        read.extend(gyroscope)
        read.extend(magnetic_field)
        read.extend(orientation)
        read.extend(linear_acc)
        read.extend(gravity)
        read.extend(rotation_vector)

        return np.array(read)

    @staticmethod
    def _get_readings(message_list):
        readings = []
        if len(message_list) > 0:
            message_list = [message.decode("utf-8") for message in message_list]
            for data_list in list(csv.reader(message_list, skipinitialspace=True)):
                readings.append(DataCollector._get_read(data_list))
        readings = np.array(readings)
        if len(readings)>1:
            return readings[np.argsort(readings[:,0])]
        return readings

    def record(self):
        self.recorded_messages = []
        self.started = True
        self.recoding = True

    def get_last_result(self):
        return DataCollector._get_readings(self.last_messages)

    def stop(self):
        self.recoding = False
        return DataCollector._get_readings(self.recorded_messages)
