import streamlit as st

from model import DetectedFaces


DETECTED_FACES_2 = "DETECTED_FACES_2"


class DetectedFaces2SState:
    @staticmethod
    def get() -> DetectedFaces:
        return st.session_state[DETECTED_FACES_2]

    @staticmethod
    def set(detected_faces: DetectedFaces) -> None:
        st.session_state[DETECTED_FACES_2] = detected_faces

    @classmethod
    def clear(cls) -> None:
        if cls.is_set_already():
            del st.session_state[DETECTED_FACES_2]

    @staticmethod
    def is_set_already() -> bool:
        if DETECTED_FACES_2 in st.session_state:
            return True
        else:
            return False
