import streamlit as st

from model import ConbinedImage


CONBINED_IMAGE = "CONBINED_IMAGE"


class ConbinedImageSState:
    @staticmethod
    def get() -> ConbinedImage:
        return st.session_state[CONBINED_IMAGE]

    @staticmethod
    def set(conbined_image: ConbinedImage) -> None:
        st.session_state[CONBINED_IMAGE] = conbined_image

    @classmethod
    def clear(cls) -> None:
        if cls.is_set_already():
            del st.session_state[CONBINED_IMAGE]

    @staticmethod
    def is_set_already() -> bool:
        if CONBINED_IMAGE in st.session_state:
            return True
        else:
            return False
