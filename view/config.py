import streamlit as st

from model import LOGO_SVG


class AppConfig:
    @staticmethod
    def set_app_config() -> None:
        st.set_page_config(
            page_title="Do We Look Alike?",
            page_icon=LOGO_SVG,
            layout="centered",
        )
