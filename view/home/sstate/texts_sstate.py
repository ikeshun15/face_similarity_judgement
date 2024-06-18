import streamlit as st

from ..texts import Texts


TEXTS = "TEXTS"


class TextsSState:
    @staticmethod
    def get() -> Texts:
        return st.session_state[TEXTS]

    @staticmethod
    def set(texts: Texts) -> None:
        st.session_state[TEXTS] = texts

    @staticmethod
    def is_initialized_already() -> bool:
        if TEXTS in st.session_state:
            return True
        else:
            return False
