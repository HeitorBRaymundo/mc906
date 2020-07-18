from data import Data
from data_collector import DataCollector
from enumerations import Author, Device, Spell
from utils import KeyListener, user_confirmation, print_local_ip

AUTHOR = Author.ANDERSON
DEVICE = Device.SAMSUNG_A5
SPELL = Spell.INCENDIO
AUTO_SAVE_CONTINUE = True

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
        print(times_sub)

        if max(times_sub) < 0.1:
            data = Data(readings, SPELL, AUTHOR, DEVICE)

            if AUTO_SAVE_CONTINUE or user_confirmation("Deseja salvar?"):
                data.save()
            else:
                print("Operação salvar cancelada. ")

            if not AUTO_SAVE_CONTINUE and not user_confirmation("Continuar capturando novos dados?"):
                break
        else:
            print("ERRO: DELAY SUPERIOR A 0.1s ENTRE AS MENSAGENS!!! ")
    else:
        print("ERRO: LEITURA MENOR QUE 20 DADOS!!! ")
