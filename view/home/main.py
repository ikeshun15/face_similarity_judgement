import streamlit as st
from streamlit_lottie import st_lottie_spinner

from model import UserFaces, FaceRecognizerFactory, PROCCESSING_LOTTIE
from .sstate import TextsSState
from .texts import Texts


class HomeView:
    @staticmethod
    def init():
        if not TextsSState.is_initialized_already():
            TextsSState.set(texts=Texts(lang="jp"))

        texts = TextsSState.get()
        with st.spinner(text=texts.downloading_model):
            FaceRecognizerFactory.download_model_if_not_exists()

    @staticmethod
    def change_lang_callback():
        texts = TextsSState.get()
        if texts.is_en:
            TextsSState.set(texts=Texts(lang="jp"))
        elif texts.is_jp:
            TextsSState.set(texts=Texts(lang="en"))

    @classmethod
    def page_header_components(cls):
        texts = TextsSState.get()
        style = "<style>h3 {text-align: center;}</style>"
        st.markdown(style, unsafe_allow_html=True)
        st.markdown(f"### {texts.title}")
        _, right = st.columns([3, 1])
        with right:
            st.button(label=texts.change_lang, on_click=cls.change_lang_callback, use_container_width=True)

    @staticmethod
    def page_footer_components():
        texts = TextsSState.get()
        style = "<style>p {text-align: center;}</style>"
        st.markdown(style, unsafe_allow_html=True)
        st.markdown(texts.authers)

    @staticmethod
    def image_components():
        texts = TextsSState.get()

        with st.form(key="image_input_form"):
            ok_types = ["png", "jpg", "jpeg", "bmp", "webp", "heic"]
            uploaded_file1 = st.file_uploader(label=texts.photo_of_person1, type=ok_types, accept_multiple_files=False, label_visibility="collapsed")
            uploaded_file2 = st.file_uploader(label=texts.photo_of_person2, type=ok_types, accept_multiple_files=False, label_visibility="collapsed")
            left, _ = st.columns([1, 3])
            with left:
                submit_button = st.form_submit_button(label=texts.analyze, type="primary", use_container_width=True)

        if submit_button:
            with st_lottie_spinner(animation_source=PROCCESSING_LOTTIE, height=200):
                if not uploaded_file1:
                    st.warning(icon="🙅", body=texts.please_upload_photo_of_person1)
                    return
                if not uploaded_file2:
                    st.warning(icon="🙅", body=texts.please_upload_photo_of_person2)
                    return

                user_faces = UserFaces(uploaded_image1=uploaded_file1, uploaded_image2=uploaded_file2)
                try:
                    combined_image = user_faces.analyze()
                    st.image(combined_image, use_column_width=True)
                except:
                    st.error(icon="🙅", body=texts.only_one_person)

    @classmethod
    def display_components(cls) -> None:
        cls.init()
        cls.page_header_components()
        cls.image_components()
        cls.page_footer_components()
