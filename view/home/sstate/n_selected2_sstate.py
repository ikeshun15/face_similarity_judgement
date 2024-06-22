import streamlit as st


N_SELECTED_2 = "N_SELECTED_2"


class NSelected2SState:
    @staticmethod
    def get() -> int:
        return st.session_state[N_SELECTED_2]

    @staticmethod
    def set(n_selected: int) -> None:
        st.session_state[N_SELECTED_2] = n_selected

    @staticmethod
    def reset() -> None:
        st.session_state[N_SELECTED_2] = 0

    @staticmethod
    def count_up() -> None:
        st.session_state[N_SELECTED_2] += 1

    @classmethod
    def init(cls) -> None:
        if not N_SELECTED_2 in st.session_state:
            cls.set(n_selected=0)
