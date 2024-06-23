from enum import Enum, auto


class States(Enum):
    WAKE_UP = auto()
    DETECTE_FACES1 = auto()
    SELECT_N_FACE1 = auto()
    DETECTE_FACES2 = auto()
    SELECT_N_FACE2 = auto()
    SHOW_RESULT = auto()
