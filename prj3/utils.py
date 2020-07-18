import socket

from pynput.keyboard import Key
from pynput import keyboard

class KeyListener:

    def __init__(self):
        self.pressing_shift = False

        def on_press(key):
            if key == Key.shift:
                self.pressing_shift = True

        def on_release(key):
            if key == Key.shift:
                self.pressing_shift = False

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

    def is_pressing_shift(self):
        return self.pressing_shift

def print_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("HOST: {}".format(s.getsockname()[0]))
    s.close()

def user_confirmation(message):
    while 1:
        text = input("{} [y/n]: \n".format(message))
        if text == 'y':
            return True
        elif text == 'n':
            return False
        else:
            print("Digite 'y' ou 'n'")

