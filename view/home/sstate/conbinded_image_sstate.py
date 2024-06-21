import streamlit as st

from model import ConbindedImage


CONBINDED_IMAGE = "CONBINDED_IMAGE"


class ConbindedImageSState:
    @staticmethod
    def get() -> ConbindedImage:
        return st.session_state[CONBINDED_IMAGE]

    @staticmethod
    def set(conbinded_image: ConbindedImage) -> None:
        st.session_state[CONBINDED_IMAGE] = conbinded_image

    @classmethod
    def clear(cls) -> None:
        if cls.is_set_already():
            del st.session_state[CONBINDED_IMAGE]

    @staticmethod
    def is_set_already() -> bool:
        if CONBINDED_IMAGE in st.session_state:
            return True
        else:
            return False
