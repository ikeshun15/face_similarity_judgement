import streamlit as st

from .logo import NORMAL_LOGO_SVG


class AppConfig:
    @staticmethod
    def set_app_config() -> None:
        st.set_page_config(
            page_title="Do We Look Alike?",
            page_icon=NORMAL_LOGO_SVG,
            layout="centered",
        )
