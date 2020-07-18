from enum import Enum, auto, unique

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return str(self.value)

# Labels
class Spell(AutoName):
    INCENDIO = auto()
    WINGARDIUM_LEVIOSA = auto()
    VENTUS = auto()

class Author(AutoName):
    ANDERSON = auto()
    DIEGO = auto()
    GUILHERME = auto()
    HEITOR = auto()
    YURI = auto()

class Device(AutoName):
    SAMSUNG_A5 = auto()

