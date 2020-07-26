from enum import Enum, auto, unique

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return str(self.value)

# Labels
class Spell(AutoName):
    UNKNOWN = auto()
    WINGARDIUM_LEVIOSA = auto()
    ALOHOMORA = auto()
    ARRESTO_MOMENTUM = auto()
    FINITE_INCANTATEM = auto()
    REVELIO = auto()
    INCENDIO = auto()

class Author(AutoName):
    UNKNOWN = auto()
    TESTER = auto()
    ANDERSON = auto()
    DIEGO = auto()
    GUILHERME = auto()
    HEITOR = auto()
    YURI = auto()

class Device(AutoName):
    UNKNOWN = auto()
    SAMSUNG_A5 = auto()
    MOTO_X = auto()
    SAMSUNG_S8 = auto()
    MOTO_G5S_PLUS = auto()

