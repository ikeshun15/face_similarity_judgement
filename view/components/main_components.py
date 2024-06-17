import streamlit as st
from model import UserFace, FaceRecognizer


class MainComponents:
    @staticmethod
    def init():
        st.set_page_config(
            page_title="私たちって似てる？",
            page_icon="🥰",
            layout="wide",
        )
        with st.spinner(text="モデルダウンロード中..."):
            FaceRecognizer.download_model()

    @staticmethod
    def page_header_components():
        st.markdown("# 🥰私たちって似てる？")
        st.markdown(
            "このアプリは顔写真の類似度を判定します。 Created by [Takanari Shimbo 🦥](https://github.com/TakanariShimbo) and [Shunichi Ikezu 🍓](https://github.com/ikeshun15)"
        )

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
                if uploaded_file1 is not None and uploaded_file2 is not None:
                    user_face = UserFace(image_path1=uploaded_file1, image_path2=uploaded_file2)
                    try:
                        similarity = user_face.estimate_similarity()
                        combined_image = user_face.make_image(similarity=similarity)
                        st.image(combined_image, use_column_width=True)
                    except:
                        st.error(icon="🙅", body="誰か一人が映っている写真にしてね")

                else:
                    st.warning(icon="🙅", body="二人分の写真をアップロードしてね")

    @classmethod
    def display_components(cls) -> None:
        cls.init()
        cls.page_header_components()
        cls.image_components()
