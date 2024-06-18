import os

from dotenv import load_dotenv
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pillow_heif

from .face_recognizer import SingletonFaceRecognizer

load_dotenv()


FONT_TYPE = os.environ["FONT_TYPE"]
HEART_IMAGE_PATH = "./data/heart.png"


class UserFaces:
    def __init__(self, uploaded_image1, uploaded_image2):
        self._face_recognizer = SingletonFaceRecognizer()

        self._original_image1 = self._open_image(uploaded_image1).convert("RGB")
        self._original_image2 = self._open_image(uploaded_image2).convert("RGB")

        self._image1 = np.array(self._original_image1)
        self._image2 = np.array(self._original_image2)

    def analyze(self):
        similarity = self._estimate_similarity()
        self._make_image(similarity=similarity)

    @staticmethod
    def _open_image(uploaded_image):
        file_extension = uploaded_image.name.split(".")[-1].lower()

        if file_extension == "heic":
            heif_file = pillow_heif.read_heif(uploaded_image)
            return Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
        else:
            return Image.open(uploaded_image)

    def _estimate_similarity(self) -> int:
        embedding1 = self._face_recognizer.detect_and_encode_face(image=self._image1)
        embedding2 = self._face_recognizer.detect_and_encode_face(image=self._image2)

        assert type(embedding1) == np.ndarray
        assert type(embedding2) == np.ndarray

        cosine_similarity = self._face_recognizer.estimate_cosine_similarity(embedding1=embedding1, embedding2=embedding2)
        percent_similarity = self._convert_cosine_to_percent(cosine_value=cosine_similarity)
        return percent_similarity

    def _make_image(self, similarity: int = 50, new_width: int = 2200, new_height: int = 450):
        image_scale = 0.5 * (similarity + 1) / 100

        left_image = self._original_image1.convert("RGBA")
        right_image = self._original_image2.convert("RGBA")

        left_image_ratio = left_image.width / left_image.height
        right_image_ratio = right_image.width / right_image.height

        new_left_width = int(new_height * left_image_ratio)
        new_right_width = int(new_height * right_image_ratio)

        left_image = left_image.resize((new_left_width, new_height))
        right_image = right_image.resize((new_right_width, new_height))

        middle_image = Image.open(HEART_IMAGE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(middle_image)
        font = ImageFont.truetype(FONT_TYPE, 80)
        draw.text((130, 150), f"{similarity}%", fill="black", font=font)

        width, height = middle_image.size
        middle_image = middle_image.resize((int(width * image_scale * 2.5), int(height * image_scale * 2.5)))

        new_image = Image.new("RGBA", (new_width, new_height))

        new_image.paste(left_image, ((new_width // 3 - new_left_width) // 2, (new_height - left_image.height) // 2))
        new_image.paste(middle_image, ((new_width // 3 - middle_image.width) // 2 + new_width // 3, (new_height - middle_image.height) // 2), middle_image)
        new_image.paste(right_image, ((new_width // 3 - new_right_width) // 2 + new_width * 2 // 3, (new_height - right_image.height) // 2))

        return new_image

    @staticmethod
    def _convert_cosine_to_percent(cosine_value: float) -> int:
        percent_value = (abs(cosine_value) ** (2 / 3)) * 150 + 30
        if cosine_value > 0:
            return int(min(percent_value, 100))
        else:
            return int(max(percent_value, 0))
