import streamlit as st
from model import UserFace, ModelManager

class MainComponents:
    @staticmethod
    def init():
        st.set_page_config(
            page_title="Face Similarity Judgement",
            page_icon="🥰",
            layout="wide",
        )
        with st.spinner(text="モデルダウンロード中..."):
            ModelManager.ONNX

    @staticmethod
    def page_header_components():
        st.markdown("# 🥰 Face Similarity Judgement")
        st.markdown("このアプリは顔写真の類似度を判定します。")
    
    @staticmethod
    def image_components():
        form = st.form(key="image_input_form")
        with form:
            col1, col2 = st.columns(2)
            uploaded_file1 = col1.file_uploader("1枚目の写真", type=["png", "jpg", "jpeg"])
            uploaded_file2 = col2.file_uploader("2枚目の写真", type=["png", "jpg", "jpeg"])
            submit_button = st.form_submit_button(label='判定する✨', type="primary")

        if submit_button:
            with st.spinner(text="計算中..."):
                if uploaded_file1 is not None and uploaded_file2 is not None:
                    face = UserFace(image_path1=uploaded_file1, image_path2=uploaded_file2)
                    is_detect = face.detect_faces()
                    
                    if is_detect:
                        similarity = face.estimate_cosine_similarity()
                        combined_image = face.make_image(scale=similarity)
                        st.image(combined_image, use_column_width=True)
                    else:
                        st.error(icon="🙅", body="顔を検出できませんでした")
                else:
                    st.warning(icon="🙅", body="二枚の画像をアップロードしてください")

    @classmethod
    def display_components(cls) -> None:
        cls.init()
        cls.page_header_components()
        cls.image_components()