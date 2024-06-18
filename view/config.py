import streamlit as st


class AppConfig:
    @staticmethod
    def set_app_config():
        st.set_page_config(
            page_title="Do We Look Alike?",
            page_icon="🥰",
            layout="wide",
        )
