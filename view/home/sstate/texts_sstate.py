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

    @classmethod
    def change_lang(cls) -> None:
        texts = cls.get()
        st.session_state[TEXTS] = Texts.get_another_texts(texts=texts)

    @classmethod
    def init(cls) -> None:
        if not TEXTS in st.session_state:
            init_texts = Texts(lang="jp")
            cls.set(texts=init_texts)
