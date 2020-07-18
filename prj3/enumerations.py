from enum import Enum, auto, unique

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return str(self.value)

# Labels
class Spell(AutoName):
    WINGARDIUM_LEVIOSA = auto()
    ALOHOMORA = auto()
    ARRESTO_MOMENTUM = auto()
    FINITE_INCANTATEM = auto()
    REVELIO = auto()
    INCENDIO = auto()

class Author(AutoName):
    ANDERSON = auto()
    DIEGO = auto()
    GUILHERME = auto()
    HEITOR = auto()
    YURI = auto()

class Device(AutoName):
    SAMSUNG_A5 = auto()
    MOTO_X = auto()

