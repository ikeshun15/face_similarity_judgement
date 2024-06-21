from PIL import Image
import pillow_heif
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_lottie import st_lottie_spinner

from model import download_model_if_not_exists, PROCESSING_LOTTIE, DetectedFaces, ConbindedImage
from .sstate import StatesSState, DetectedFaces1SState, DetectedFaces2SState, NSelected1SState, NSelected2SState, TextsSState, ConbindedImageSState
from .states import States
from .texts import Texts


class HomeView:
    @staticmethod
    def init():
        with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
            download_model_if_not_exists()

        if not TextsSState.is_initialized_already():
            TextsSState.set(texts=Texts(lang="en"))

        if not NSelected1SState.is_initialized_already():
            NSelected1SState.set(n_selected=0)

        if not NSelected2SState.is_initialized_already():
            NSelected2SState.set(n_selected=0)

        if not StatesSState.is_initialized_already():
            StatesSState.set(state=States.SET_DETECTED_FACES_1)

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

    @classmethod
    def set_detected_faces_1_components(cls) -> bool:
        texts = TextsSState.get()
        st.markdown(body=f"###### {texts.image1_uploader}")

        ok_types = ["png", "jpg", "jpeg", "bmp", "webp", "heic"]
        uploaded_file = st.file_uploader(label=texts.photo_of_person1, type=ok_types, accept_multiple_files=False, label_visibility="collapsed")

        if uploaded_file is not None:
            with st.spinner(text=texts.loading):
                image_rgb = cls._open_image_as_rgb(uploaded_image=uploaded_file)
                detected_faces = DetectedFaces.detect(image_rgb=image_rgb)

            if detected_faces.n_faces == 0:
                st.error(icon="🙅", body=texts.more_than_one_person)
                return False

            DetectedFaces1SState.set(detected_faces=detected_faces)
            if detected_faces.n_faces == 1:
                StatesSState.set(state=States.SET_DETECTED_FACES_2)
            else:
                StatesSState.set(state=States.SELECT_N_FACE_1)
            return True

        return False

    @classmethod
    def select_n_face_1_components(cls) -> bool:
        texts = TextsSState.get()
        st.markdown(body=f"###### {texts.image1_selector}")

        n_selected_1 = NSelected1SState.get()
        detected_faces = DetectedFaces1SState.get()
        face_image = detected_faces.get_face_image(n=n_selected_1, trim_factor=1.5, dsize=(500, 500))
        _, center, _ = st.columns(3)
        with center:
            st.image(image=face_image)

        left, _, center, _, right = st.columns([1, 0.5, 1, 0.5, 1])
        with left:
            is_back = st.button(label=texts.back, use_container_width=True)
        with center:
            is_other = st.button(label=texts.other, use_container_width=True)
        with right:
            is_next = st.button(label=texts.next, use_container_width=True)

        if is_back:
            StatesSState.set(state=States.SET_DETECTED_FACES_1)
            return True
        elif is_other:
            if NSelected1SState.get() < detected_faces.n_faces - 1:
                NSelected1SState.count_up()
            else:
                NSelected1SState.reset()
            return True
        elif is_next:
            StatesSState.set(state=States.SET_DETECTED_FACES_2)
            return True

        return False

    @classmethod
    def set_detected_faces_2_components(cls) -> bool:
        texts = TextsSState.get()
        st.markdown(body=f"###### {texts.image1_uploader}")

        ok_types = ["png", "jpg", "jpeg", "bmp", "webp", "heic"]
        uploaded_file = st.file_uploader(label=texts.photo_of_person2, type=ok_types, accept_multiple_files=False, label_visibility="collapsed")

        left, _ = st.columns([1, 3])
        with left:
            is_back = st.button(label=texts.back, use_container_width=True)

        if uploaded_file is not None:
            with st.spinner(text=texts.loading):
                image_rgb = cls._open_image_as_rgb(uploaded_image=uploaded_file)
                detected_faces = DetectedFaces.detect(image_rgb=image_rgb)

            if detected_faces.n_faces == 0:
                st.error(icon="🙅", body=texts.more_than_one_person)
                return False

            DetectedFaces2SState.set(detected_faces=detected_faces)
            if detected_faces.n_faces == 1:
                StatesSState.set(state=States.SHOW_RESULT)
            else:
                StatesSState.set(state=States.SELECT_N_FACE_2)
            return True

        if is_back:
            StatesSState.set(state=States.SELECT_N_FACE_1)
            return True
        return False

    @classmethod
    def select_n_face_2_components(cls) -> bool:
        texts = TextsSState.get()
        st.markdown(body=f"###### {texts.image2_selector}")

        n_selected_2 = NSelected2SState.get()
        detected_faces = DetectedFaces2SState.get()
        face_image = detected_faces.get_face_image(n=n_selected_2, trim_factor=1.5, dsize=(500, 500))
        _, center, _ = st.columns(3)
        with center:
            st.image(image=face_image)

        left, _, center, _, right = st.columns([1, 0.5, 1, 0.5, 1])
        with left:
            is_back = st.button(label=texts.back, use_container_width=True)
        with center:
            is_other = st.button(label=texts.other, use_container_width=True)
        with right:
            is_next = st.button(label=texts.next, use_container_width=True)

        if is_back:
            StatesSState.set(state=States.SET_DETECTED_FACES_2)
            return True
        elif is_other:
            if NSelected2SState.get() < detected_faces.n_faces - 1:
                NSelected2SState.count_up()
            else:
                NSelected2SState.reset()
            return True
        elif is_next:
            StatesSState.set(state=States.SHOW_RESULT)
            return True

        return False

    @classmethod
    def show_result_components(cls) -> bool:
        texts = TextsSState.get()
        st.markdown(body=f"###### {texts.result}")

        if not ConbindedImageSState.is_set_already():
            detected_faces1 = DetectedFaces1SState.get()
            n_selected1 = NSelected1SState.get()
            detected_faces2 = DetectedFaces2SState.get()
            n_selected2 = NSelected2SState.get()

            with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
                conbined_image = ConbindedImage.based_similarity(
                    detected_faces1=detected_faces1, n_selected1=n_selected1, detected_faces2=detected_faces2, n_selected2=n_selected2
                )

            ConbindedImageSState.set(conbinded_image=conbined_image)

        st.image(ConbindedImageSState.get().image, use_column_width=True)
        st.balloons()

        _, center, _ = st.columns([1.5, 1, 1.5])
        with center:
            is_retry = st.button(label=texts.retry, use_container_width=True)

        if is_retry:
            ConbindedImageSState.clear()
            DetectedFaces1SState.clear()
            DetectedFaces2SState.clear()
            NSelected1SState.reset()
            NSelected2SState.reset()
            StatesSState.set(state=States.SET_DETECTED_FACES_1)
            return True

        return False

    @classmethod
    def display_components(cls) -> None:
        cls.init()
        cls.page_header_components()
        if StatesSState.get() == States.SET_DETECTED_FACES_1:
            is_call_rerun = cls.set_detected_faces_1_components()
        elif StatesSState.get() == States.SELECT_N_FACE_1:
            is_call_rerun = cls.select_n_face_1_components()
        elif StatesSState.get() == States.SET_DETECTED_FACES_2:
            is_call_rerun = cls.set_detected_faces_2_components()
        elif StatesSState.get() == States.SELECT_N_FACE_2:
            is_call_rerun = cls.select_n_face_2_components()
        else:
            is_call_rerun = cls.show_result_components()
        cls.page_footer_components()

        if is_call_rerun:
            st.rerun()

    @staticmethod
    def _open_image_as_rgb(uploaded_image: UploadedFile) -> Image.Image:
        uploaded_image_name: str = uploaded_image.name
        file_extension = uploaded_image_name.split(".")[-1].lower()

        if file_extension == "heic":
            heif_file = pillow_heif.read_heif(uploaded_image)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
        else:
            image = Image.open(uploaded_image)

        return image.convert("RGB")
