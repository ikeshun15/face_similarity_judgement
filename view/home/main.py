import streamlit as st
from model import UserFaces, FaceRecognizer


class HomeView:
    @staticmethod
    def init():
        with st.spinner(text="モデルダウンロード中..."):
            FaceRecognizer.download_model_if_not_exists()

    @staticmethod
    def page_header_components():
        st.markdown("## 🥰私たちって似てる？")
        st.markdown("Created by [Takanari Shimbo 🦥](https://github.com/TakanariShimbo) and [Shunichi Ikezu 🍓](https://github.com/ikeshun15)")

    @staticmethod
    def image_components():
        form = st.form(key="image_input_form")
        with form:
            col1, col2 = st.columns(2)
            uploaded_file1 = col1.file_uploader("1枚目の写真", type=["png", "jpg", "jpeg"])
            uploaded_file2 = col2.file_uploader("2枚目の写真", type=["png", "jpg", "jpeg"])
            submit_button = st.form_submit_button(label="判定する✨", type="primary")

        if submit_button:
            with st.spinner(text="計算中..."):
                if not uploaded_file1:
                    st.warning(icon="🙅", body="一人目の写真をアップロードしてね")
                if not uploaded_file2:
                    st.warning(icon="🙅", body="二人目の写真をアップロードしてね")

                user_faces = UserFaces(image_path1=uploaded_file1, image_path2=uploaded_file2)
                try:
                    similarity = user_faces.estimate_similarity()
                    combined_image = user_faces.make_image(similarity=similarity)
                    st.image(combined_image, use_column_width=True)
                except:
                    st.error(icon="🙅", body="誰か一人が映っている写真にしてね")

    @classmethod
    def display_components(cls) -> None:
        cls.init()
        cls.page_header_components()
        cls.image_components()
