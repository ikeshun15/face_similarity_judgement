import streamlit as st

from ..states import States


STATES = "STATES"


class StatesSState:
    @staticmethod
    def get() -> States:
        return st.session_state[STATES]

    @staticmethod
    def set(state: States) -> None:
        st.session_state[STATES] = state

    @staticmethod
    def is_initialized_already() -> bool:
        if STATES in st.session_state:
            return True
        else:
            return False
