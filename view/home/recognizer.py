import numpy as np
from PIL import Image
import pillow_heif
from streamlit.runtime.uploaded_file_manager import UploadedFile

from model import FaceRecognizerFactory, DetectedFaces, ConbinedImage


def detect_faces(
    uploaded_image: UploadedFile,
) -> DetectedFaces:
    image_rgb = _open_image_as_rgb(uploaded_image=uploaded_image)
    np_image_rgb = np.array(image_rgb, dtype=np.uint8)
    face_recognizer = FaceRecognizerFactory.create_as_singleton()
    faces = face_recognizer.detect_faces(image_rgb=np_image_rgb)
    return DetectedFaces(image_rgb=np_image_rgb, faces=faces)


def conbine_images_based_similarity(
    detected_faces1: DetectedFaces,
    n_selected1: int,
    detected_faces2: DetectedFaces,
    n_selected2: int,
) -> ConbinedImage:
    face1 = detected_faces1.get_face(n=n_selected1)
    face2 = detected_faces2.get_face(n=n_selected2)
    image_rgb_1 = detected_faces1.get_face_image(n=n_selected1, trim_factor=2.0, dsize=(500, 500))
    image_rgb_2 = detected_faces2.get_face_image(n=n_selected2, trim_factor=2.0, dsize=(500, 500))
    face_recognizer = FaceRecognizerFactory.create_as_singleton()
    cosine_similarity = face_recognizer.encode_faces_and_estimate_cosine_similarity(
        image_rgb1=detected_faces1.image_rgb, face1=face1, image_rgb2=detected_faces2.image_rgb, face2=face2
    )
    percent_similarity = _convert_cosine_to_percent(cosine_value=cosine_similarity)
    return ConbinedImage(
        image_rgb_1=image_rgb_1,
        image_rgb_2=image_rgb_2,
        percent_value=percent_similarity,
    )


def _convert_cosine_to_percent(cosine_value: float) -> int:
    percent_value = int((abs(cosine_value) ** (2 / 3)) * 150 + 30)
    if percent_value > 100:
        percent_value = 100
    if percent_value < 0:
        percent_value = 0
    return percent_value


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
