import streamlit as st

from model import ImageManager

class HomeComponents:
    @staticmethod
    def init():
        st.set_page_config(
            page_title="Face Similarity Judgement",
            page_icon="🥰",
            layout="wide",
        )

    
    @staticmethod
    def main_page():
        st.markdown("# 🥰 Face Similarity Judgement")
        form = st.form(key="image_input_form")

        with form:
            uploaded_file1 = st.file_uploader("画像をアップロードしてください1", type=["png", "jpg", "jpeg"])
            uploaded_file2 = st.file_uploader("画像をアップロードしてください2", type=["png", "jpg", "jpeg"])
            scale = st.slider(label="test", min_value=0.1, max_value=2.0, step=0.1)
            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if uploaded_file1 is not None and uploaded_file2 is not None:
                composite_image = ImageManager.make_image(image1_path=uploaded_file1, image2_path=uploaded_file2, scale=scale)

                st.image(composite_image, caption='Image', use_column_width=True)
            else:
                st.write("画像がアップロードされていません。")

    @classmethod
    def display_components(cls):
        cls.init()
        cls.main_page()