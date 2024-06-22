import streamlit as st


N_SELECTED_1 = "N_SELECTED_1"


class NSelected1SState:
    @staticmethod
    def get() -> int:
        return st.session_state[N_SELECTED_1]

    @staticmethod
    def set(n_selected: int) -> None:
        st.session_state[N_SELECTED_1] = n_selected

    @staticmethod
    def reset() -> None:
        st.session_state[N_SELECTED_1] = 0

    @staticmethod
    def count_up() -> None:
        st.session_state[N_SELECTED_1] += 1

    @classmethod
    def init(cls) -> None:
        if not N_SELECTED_1 in st.session_state:
            cls.set(n_selected=0)
