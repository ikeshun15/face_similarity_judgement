from enum import Enum, auto


class States(Enum):
    WAKE_UP = auto()
    SET_DETECTED_FACES_1 = auto()
    SELECT_N_FACE_1 = auto()
    SET_DETECTED_FACES_2 = auto()
    SELECT_N_FACE_2 = auto()
    SHOW_RESULT = auto()
