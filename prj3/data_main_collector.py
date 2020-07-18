from data import Data
from data_collector import DataCollector
from enumerations import Author, Device, Spell
from utils import KeyListener, user_confirmation, print_local_ip
import numpy as np

AUTHOR = Author.HEITOR
DEVICE = Device.MOTO_X
SPELL = Spell.INCENDIO

key_listener = KeyListener()

print_local_ip()

dc = DataCollector()

while 1:
    print("Segure SHIFT para capturar movimento.")

    while not key_listener.is_pressing_shift():
        pass

    dc.record()

    while key_listener.is_pressing_shift():
        pass

    readings = dc.stop()

    if len(readings) > 20:

        print("Foram capurados {} dados, totalizando {:.2f} segundos. ".format(len(readings), readings[-1][0]-readings[0][0]))
        times_sub = readings[1:, 0][::-1] - readings[:-1, 0][::-1]
        #print(np.sort(times_sub))

        incomplete_ratio = np.count_nonzero(np.isnan(readings))/readings.size
        data = Data(readings, SPELL, AUTHOR, DEVICE)

        if incomplete_ratio > 0.1:
            print("ATENÇÃO: MUITAS MENSAGENS IMCOMPLETAS!!! Taxa: {}".format(incomplete_ratio))

        if max(times_sub) > 0.1:
            print("ATENÇÃO: DELAY SUPERIOR A 0.1s ENTRE AS MENSAGENS!!!")

        if user_confirmation("Deseja salvar?"):
            data.save()
            print("DADOS SALVOS!!! ")
        else:
            print("Operação salvar cancelada. ")

    else:
        print("ERRO: LEITURA MENOR QUE 20 DADOS!!! ")
