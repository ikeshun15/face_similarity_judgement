import streamlit as st

class HomeComponents:
    @staticmethod
    def init():
        st.set_page_config(
            page_title="Face Similarity Judgement",
            page_icon="🥰",
            layout="wide",
        )

    @staticmethod
    def page_header():
        st.markdown("# 🥰 Face Similarity Judgement")
        st.markdown("このアプリは顔写真の類似度を判定します。")

    @staticmethod
    def upload_images():
        form = st.form(key="image_input_form")
        uploaded_file1 = None
        uploaded_file2 = None
        submit_pressed = False
        with form:
            col1, col2 = st.columns(2)
            uploaded_file1 = col1.file_uploader("一人目の写真", type=["png", "jpg", "jpeg"])
            uploaded_file2 = col2.file_uploader("二人目の写真", type=["png", "jpg", "jpeg"])
            submit_button = st.form_submit_button(label='Submit', type="primary")

        if submit_button:
            submit_pressed = True
        return uploaded_file1, uploaded_file2, submit_pressed

    @staticmethod
    def display_images(image1, image2):
        st.image(image1, caption='Uploaded Image 1.', use_column_width=True)
        st.image(image2, caption='Uploaded Image 2.', use_column_width=True)

    @staticmethod
    def display_error(message):
        st.error(icon="🙅", body=message)

    @staticmethod
    def display_combined_image(image):
        st.image(image, use_column_width=True)