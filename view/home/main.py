import time

import streamlit as st
from streamlit_lottie import st_lottie_spinner

from model import download_model_if_not_exists, PROCESSING_LOTTIE, LOGO_LARGE_SVG
from .sstate import StatesSState, DetectedFaces1SState, DetectedFaces2SState, NSelected1SState, NSelected2SState, TextsSState, ConbinedImageSState
from .states import States
from .recognizer import detect_faces, conbine_images_based_similarity


OK_IMAGE_EXTS = ["png", "jpg", "jpeg", "bmp", "webp", "heic"]
TEMP_TRIM_FACTOR = 1.5
TEMP_DSIZE = (500, 500)


class HomeView:
    @staticmethod
    def init():
        with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
            download_model_if_not_exists()

        TextsSState.init()
        NSelected1SState.init()
        NSelected2SState.init()
        StatesSState.init()

    @staticmethod
    def wakeup_components():
        with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
            time.sleep(1)
            StatesSState.set(state=States.DETECTE_FACES1)

    @classmethod
    def page_header_components(cls):
        texts = TextsSState.get()
        st.markdown(
            "<style>h3 {text-align: center;}</style>" + f"<h3>{LOGO_LARGE_SVG} {texts.title}</h3>",
            unsafe_allow_html=True,
        )

        _, right = st.columns([3, 1])
        with right:
            st.button(
                label=texts.change_lang,
                use_container_width=True,
                on_click=lambda: TextsSState.change_lang(),
            )

        st.markdown(
            """
            <style>
            .stProgress .st-bo {
                background-color: "#e0aaa0";
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        if StatesSState.get() == States.DETECTE_FACES1:
            progress = 1
        elif StatesSState.get() == States.SELECT_N_FACE1:
            progress = 26
        elif StatesSState.get() == States.DETECTE_FACES2:
            progress = 51
        elif StatesSState.get() == States.SELECT_N_FACE2:
            progress = 76
        elif StatesSState.get() == States.SHOW_RESULT:
            progress = 100
        else:
            raise Exception("Unexpected states!")

        p = st.progress(value=progress)
        p.progress(value=progress)

    @staticmethod
    def page_footer_components():
        texts = TextsSState.get()

        style = "<style>p {text-align: center;}</style>"
        st.markdown(style, unsafe_allow_html=True)
        st.markdown(texts.footer)

    @classmethod
    def detect_faces1_components(cls) -> bool:
        texts = TextsSState.get()
        is_detected_faces1_already = DetectedFaces1SState.is_set_already()

        st.markdown(body=f"###### {texts.uploade_or_take_image1}")

        uploaded_file = st.file_uploader(
            label="uploader",
            type=OK_IMAGE_EXTS,
            accept_multiple_files=False,
            label_visibility="collapsed",
        )

        taken_file = st.camera_input(
            label="taker",
            label_visibility="collapsed",
        )

        image_file = None
        if uploaded_file is not None:
            image_file = uploaded_file
        elif taken_file is not None:
            image_file = taken_file

        _, right = st.columns([3, 1])
        with right:
            st.button(
                key="detect_faces1_next",
                label=texts.next,
                use_container_width=True,
                disabled=False if is_detected_faces1_already else True,
                on_click=lambda: StatesSState.set(state=States.SELECT_N_FACE1),
            )

        if image_file is not None:
            with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
                detected_faces1 = detect_faces(image_file=image_file)

                if detected_faces1.n_faces == 0:
                    st.warning(body=texts.warning_no_person)
                    return False

                DetectedFaces1SState.set(detected_faces=detected_faces1)
                StatesSState.set(state=States.SELECT_N_FACE1)
                NSelected1SState.reset()
            return True

        return False

    @classmethod
    def select_n_face1_components(cls) -> bool:
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
                key="select_faces1_back",
                label=texts.back,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.DETECTE_FACES1),
            )
        with center:
            st.button(
                key="select_faces1_others",
                label=texts.others,
                use_container_width=True,
                disabled=True if detected_faces1.n_faces == 1 else False,
                on_click=lambda: NSelected1SState.count_up() if n_selected1 < detected_faces1.n_faces - 1 else NSelected1SState.reset(),
            )
        with right:
            st.button(
                key="select_faces1_next",
                label=texts.next,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.DETECTE_FACES2),
            )
        return False

    @classmethod
    def detect_faces2_components(cls) -> bool:
        texts = TextsSState.get()
        detected_faces1 = DetectedFaces1SState.get()
        is_detected_faces2_already = DetectedFaces2SState.is_set_already()

        st.markdown(body=f"###### {texts.uploade_or_take_image2}")

        uploaded_file = st.file_uploader(
            label="uploader",
            type=OK_IMAGE_EXTS,
            accept_multiple_files=False,
            label_visibility="collapsed",
        )

        taken_file = st.camera_input(
            label="taker",
            label_visibility="collapsed",
        )

        image_file = None
        if uploaded_file is not None:
            image_file = uploaded_file
        elif taken_file is not None:
            image_file = taken_file

        left, _, right = st.columns([1, 2, 1])
        with left:
            st.button(
                key="detect_faces2_back",
                label=texts.back,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.SELECT_N_FACE1),
            )

        with right:

            def _callback():
                if not is_detected_faces2_already:
                    DetectedFaces2SState.set(detected_faces=detected_faces1)
                StatesSState.set(state=States.SELECT_N_FACE2)

            if is_detected_faces2_already:
                disabled = False
            else:
                disabled = True if detected_faces1.n_faces == 1 else False
            st.button(
                key="detect_faces2_next",
                label=texts.next,
                use_container_width=True,
                disabled=disabled,
                on_click=_callback,
            )

        if image_file is not None:
            with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
                detected_faces2 = detect_faces(image_file=image_file)

                if detected_faces2.n_faces == 0:
                    st.warning(body=texts.warning_no_person)
                    return False

                DetectedFaces2SState.set(detected_faces=detected_faces2)
                NSelected2SState.reset()
                StatesSState.set(state=States.SELECT_N_FACE2)
            return True

        return False

    @classmethod
    def select_n_face2_components(cls) -> bool:
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
                key="select_faces2_back",
                label=texts.back,
                use_container_width=True,
                on_click=lambda: StatesSState.set(state=States.DETECTE_FACES2),
            )
        with center:
            st.button(
                key="select_faces2_others",
                label=texts.others,
                use_container_width=True,
                disabled=True if detected_faces2.n_faces == 1 else False,
                on_click=lambda: NSelected2SState.count_up() if n_selected2 < detected_faces2.n_faces - 1 else NSelected2SState.reset(),
            )
        with right:
            is_next = st.button(
                key="select_faces2_next",
                label=texts.next,
                use_container_width=True,
                disabled=True if is_selected_same_face else False,
            )

        if is_selected_same_face:
            st.warning(body=texts.warning_same_person)

        if is_next:
            with st_lottie_spinner(animation_source=PROCESSING_LOTTIE, height=200):
                conbined_image = conbine_images_based_similarity(
                    detected_faces1=detected_faces1,
                    n_selected1=n_selected1,
                    detected_faces2=detected_faces2,
                    n_selected2=n_selected2,
                )
                ConbinedImageSState.set(conbined_image=conbined_image)
                StatesSState.set(state=States.SHOW_RESULT)
            return True

        return False

    @classmethod
    def show_result_components(cls) -> bool:
        texts = TextsSState.get()
        conbined_image = ConbinedImageSState.get()

        st.markdown(body=f"###### {texts.result}")
        st.image(conbined_image.image, use_column_width=True)
        st.balloons()

        _, center, _ = st.columns([1.5, 1, 1.5])
        with center:

            def _callback():
                ConbinedImageSState.clear()
                DetectedFaces1SState.clear()
                DetectedFaces2SState.clear()
                NSelected1SState.reset()
                NSelected2SState.reset()
                StatesSState.set(state=States.DETECTE_FACES1)

            st.button(
                key="show_result_retry",
                label=texts.retry,
                use_container_width=True,
                on_click=_callback,
            )

        return False

    @classmethod
    def display_components(cls) -> None:
        cls.init()

        if StatesSState.get() == States.WAKE_UP:
            cls.wakeup_components()
            st.rerun()

        cls.page_header_components()

        if StatesSState.get() == States.DETECTE_FACES1:
            is_call_rerun = cls.detect_faces1_components()
        elif StatesSState.get() == States.SELECT_N_FACE1:
            is_call_rerun = cls.select_n_face1_components()
        elif StatesSState.get() == States.DETECTE_FACES2:
            is_call_rerun = cls.detect_faces2_components()
        elif StatesSState.get() == States.SELECT_N_FACE2:
            is_call_rerun = cls.select_n_face2_components()
        elif StatesSState.get() == States.SHOW_RESULT:
            is_call_rerun = cls.show_result_components()
        else:
            raise Exception("Unexpected states!")

        cls.page_footer_components()

        if is_call_rerun:
            st.rerun()
