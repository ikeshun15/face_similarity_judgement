from PIL import Image
import pillow_heif
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_lottie import st_lottie_spinner

from model import download_model_if_not_exists, PROCESSING_LOTTIE, DetectedFaces, ConbindedImage
from .sstate import StatesSState, DetectedFaces1SState, DetectedFaces2SState, NSelected1SState, NSelected2SState, TextsSState, ConbindedImageSState
from .states import States
from .texts import Texts


OK_IMAGE_EXTS = ["png", "jpg", "jpeg", "bmp", "webp", "heic"]
TEMP_TRIM_FACTOR = 1.5
TEMP_DSIZE = (500, 500)


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

    @classmethod
    def page_header_components(cls):
        texts = TextsSState.get()

        style = "<style>h3 {text-align: center;}</style>"
        st.markdown(style, unsafe_allow_html=True)
        st.markdown(f"### {texts.title}")
        _, right = st.columns([3, 1])
        with right:
            st.button(
                label=texts.change_lang,
                use_container_width=True,
                on_click=lambda: TextsSState.change_lang(),
            )

    @staticmethod
    def page_footer_components():
        texts = TextsSState.get()
        style = "<style>p {text-align: center;}</style>"
        st.markdown(style, unsafe_allow_html=True)
        st.markdown(texts.footer)

    @classmethod
    def set_detected_faces_1_components(cls) -> bool:
        texts = TextsSState.get()

        st.markdown(body=f"###### {texts.uploade_image1}")

        uploaded_file = st.file_uploader(
            label=texts.photo_of_person1,
            type=OK_IMAGE_EXTS,
            accept_multiple_files=False,
            label_visibility="collapsed",
        )

        if uploaded_file is not None:
            with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
                image_rgb = cls._open_image_as_rgb(uploaded_image=uploaded_file)
                detected_faces1 = DetectedFaces.detect(image_rgb=image_rgb)

                if detected_faces1.n_faces == 0:
                    st.warning(body=texts.warning_no_person)
                    return False

                DetectedFaces1SState.set(detected_faces=detected_faces1)

                if detected_faces1.n_faces == 1:
                    StatesSState.set(state=States.SET_DETECTED_FACES_2)
                else:
                    StatesSState.set(state=States.SELECT_N_FACE_1)
            return True

        return False

    @classmethod
    def select_n_face_1_components(cls) -> bool:
        texts = TextsSState.get()
        n_selected1 = NSelected1SState.get()
        detected_faces1 = DetectedFaces1SState.get()

        st.markdown(body=f"###### {texts.select_image1}")

        selected_face_image = detected_faces1.get_face_image(
            n=n_selected1,
            trim_factor=TEMP_TRIM_FACTOR,
            dsize=TEMP_DSIZE,
        )
        _, center, _ = st.columns(3)
        with center:
            st.image(image=selected_face_image)

        left, _, center, _, right = st.columns([1, 0.5, 1, 0.5, 1])
        with left:
            st.button(
                label=texts.back,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.SET_DETECTED_FACES_1),
            )
        with center:
            st.button(
                label=texts.others,
                use_container_width=True,
                disabled=True if detected_faces1.n_faces == 1 else False,
                on_click=lambda: NSelected1SState.count_up() if n_selected1 < detected_faces1.n_faces - 1 else NSelected1SState.reset(),
            )
        with right:
            st.button(
                label=texts.next,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.SET_DETECTED_FACES_2),
            )
        return False

    @classmethod
    def set_detected_faces_2_components(cls) -> bool:
        texts = TextsSState.get()
        detected_faces1 = DetectedFaces1SState.get()

        st.markdown(body=f"###### {texts.uploade_image2}")

        uploaded_file = st.file_uploader(
            label=texts.photo_of_person2,
            type=OK_IMAGE_EXTS,
            accept_multiple_files=False,
            label_visibility="collapsed",
        )

        left, _, right = st.columns([1, 2, 1])
        with left:
            st.button(
                label=texts.back,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.SELECT_N_FACE_1),
            )

        with right:

            def _callback():
                DetectedFaces2SState.set(detected_faces=detected_faces1)
                StatesSState.set(state=States.SELECT_N_FACE_2)

            st.button(
                label=texts.skip,
                use_container_width=True,
                disabled=True if detected_faces1.n_faces == 1 else False,
                on_click=_callback,
            )

        if uploaded_file is not None:
            with st.spinner(text=texts.loading):
                image_rgb = cls._open_image_as_rgb(uploaded_image=uploaded_file)
                detected_faces2 = DetectedFaces.detect(image_rgb=image_rgb)

                if detected_faces2.n_faces == 0:
                    st.warning(body=texts.warning_no_person)
                    return False

                DetectedFaces2SState.set(detected_faces=detected_faces2)
                if detected_faces2.n_faces == 1:
                    StatesSState.set(state=States.SHOW_RESULT)
                else:
                    StatesSState.set(state=States.SELECT_N_FACE_2)
            return True
        return False

    @classmethod
    def select_n_face_2_components(cls) -> bool:
        texts = TextsSState.get()
        n_selected1 = NSelected1SState.get()
        detected_faces1 = DetectedFaces1SState.get()
        n_selected2 = NSelected2SState.get()
        detected_faces2 = DetectedFaces2SState.get()

        st.markdown(body=f"###### {texts.select_image2}")

        selected_face_image = detected_faces2.get_face_image(
            n=n_selected2,
            trim_factor=TEMP_TRIM_FACTOR,
            dsize=TEMP_DSIZE,
        )
        _, center, _ = st.columns(3)
        with center:
            st.image(image=selected_face_image)

        is_selected_same_face = detected_faces1 == detected_faces2 and n_selected1 == n_selected2
        left, _, center, _, right = st.columns([1, 0.5, 1, 0.5, 1])
        with left:
            st.button(
                label=texts.back,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.SET_DETECTED_FACES_2),
            )
        with center:
            st.button(
                label=texts.others,
                use_container_width=True,
                disabled=True if detected_faces2.n_faces == 1 else False,
                on_click=lambda: NSelected2SState.count_up() if n_selected2 < detected_faces2.n_faces - 1 else NSelected2SState.reset(),
            )
        with right:
            is_next = st.button(
                label=texts.next,
                use_container_width=True,
                disabled=True if is_selected_same_face else False,
            )

        if is_selected_same_face:
            st.warning(body=texts.warning_same_person)

        if is_next:
            with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
                conbined_image = ConbindedImage.based_similarity(
                    detected_faces1=detected_faces1,
                    n_selected1=n_selected1,
                    detected_faces2=detected_faces2,
                    n_selected2=n_selected2,
                )
                ConbindedImageSState.set(conbinded_image=conbined_image)
                StatesSState.set(state=States.SHOW_RESULT)
            return True

        return False

    @classmethod
    def show_result_components(cls) -> bool:
        texts = TextsSState.get()
        conbinded_image = ConbindedImageSState.get()

        st.markdown(body=f"###### {texts.result}")
        st.image(conbinded_image.image, use_column_width=True)
        st.balloons()

        _, center, _ = st.columns([1.5, 1, 1.5])
        with center:

            def _callback():
                ConbindedImageSState.clear()
                DetectedFaces1SState.clear()
                DetectedFaces2SState.clear()
                NSelected1SState.reset()
                NSelected2SState.reset()
                StatesSState.set(state=States.SET_DETECTED_FACES_1)

            st.button(
                label=texts.retry,
                use_container_width=True,
                on_click=_callback,
            )

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
        elif StatesSState.get() == States.SHOW_RESULT:
            is_call_rerun = cls.show_result_components()
        else:
            is_call_rerun = cls.set_detected_faces_1_components()
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
