import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pillow_heif
from streamlit.runtime.uploaded_file_manager import UploadedFile

from .settting import Setting
from .face_recognizer import FaceRecognizerFactory


class UserFaces:
    def __init__(self, uploaded_image1: UploadedFile, uploaded_image2: UploadedFile) -> None:
        self._face_recognizer = FaceRecognizerFactory.create_as_singleton()

        self._image1 = self._open_image(uploaded_image1)
        self._image2 = self._open_image(uploaded_image2)

    def analyze(self) -> Image.Image:
        similarity = self._estimate_similarity()
        conbined_image = self._generate_conbined_image(similarity=similarity)
        return conbined_image

    @staticmethod
    def _open_image(uploaded_image: UploadedFile) -> Image.Image:
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

    def _estimate_similarity(self) -> int:
        np_image1 = np.array(self._image1)
        np_image2 = np.array(self._image2)

        embedding1 = self._face_recognizer.detect_and_encode_face(image=np_image1)
        embedding2 = self._face_recognizer.detect_and_encode_face(image=np_image2)

        assert type(embedding1) == np.ndarray
        assert type(embedding2) == np.ndarray

        cosine_similarity = self._face_recognizer.estimate_cosine_similarity(embedding1=embedding1, embedding2=embedding2)
        percent_similarity = self._convert_cosine_to_percent(cosine_value=cosine_similarity)

        return percent_similarity

    def _generate_conbined_image(self, similarity: int = 50, new_width: int = 2200, new_height: int = 450) -> Image.Image:
        image_scale = 0.5 * (similarity + 1) / 100

        left_image = self._image1.convert("RGBA")
        right_image = self._image2.convert("RGBA")

        left_image_ratio = left_image.width / left_image.height
        right_image_ratio = right_image.width / right_image.height

        new_left_width = int(new_height * left_image_ratio)
        new_right_width = int(new_height * right_image_ratio)

        left_image = left_image.resize((new_left_width, new_height))
        right_image = right_image.resize((new_right_width, new_height))

        middle_image = Image.open(Setting.HEART_IMAGE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(middle_image)
        font = ImageFont.truetype(Setting.FONT_TYPE, 80)
        draw.text((130, 150), f"{similarity}%", fill="black", font=font)

        width, height = middle_image.size
        middle_image = middle_image.resize((int(width * image_scale * 2.5), int(height * image_scale * 2.5)))

        conbined_image = Image.new("RGBA", (new_width, new_height))

        conbined_image.paste(left_image, ((new_width // 3 - new_left_width) // 2, (new_height - left_image.height) // 2))
        conbined_image.paste(middle_image, ((new_width // 3 - middle_image.width) // 2 + new_width // 3, (new_height - middle_image.height) // 2), middle_image)
        conbined_image.paste(right_image, ((new_width // 3 - new_right_width) // 2 + new_width * 2 // 3, (new_height - right_image.height) // 2))

        return conbined_image

    @staticmethod
    def _convert_cosine_to_percent(cosine_value: float) -> int:
        percent_value = (abs(cosine_value) ** (2 / 3)) * 150 + 30
        if cosine_value > 0:
            return int(min(percent_value, 100))
        else:
            return int(max(percent_value, 0))
