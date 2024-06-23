import streamlit as st

from .icon import NORMAL_ICON_SVG


class AppConfig:
    @staticmethod
    def set_app_config() -> None:
        st.set_page_config(
            page_title="Do We Look Alike?",
            page_icon=NORMAL_ICON_SVG,
            layout="centered",
        )
