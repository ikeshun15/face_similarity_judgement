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

    @classmethod
    def init(cls) -> None:
        if STATES in st.session_state:
            init_states = States.SET_DETECTED_FACES_1
            cls.set(state=init_states)
