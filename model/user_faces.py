import os

from dotenv import load_dotenv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .face_recognizer import FaceRecognizer

load_dotenv()


FONT_TYPE = os.environ["FONT_TYPE"]


class UserFaces:
    def __init__(self, image_path1, image_path2):
        self._face_recognizer = FaceRecognizer()

        self._original_image1 = Image.open(image_path1).convert("RGB")
        self._original_image2 = Image.open(image_path2).convert("RGB")

        self._image1 = np.array(self._original_image1)
        self._image2 = np.array(self._original_image2)

    def estimate_similarity(self) -> int:
        embedding1 = self._face_recognizer.detect_and_encode_face(image=self._image1)
        embedding2 = self._face_recognizer.detect_and_encode_face(image=self._image2)

        assert type(embedding1) == np.ndarray
        assert type(embedding2) == np.ndarray

        cosine_similarity = FaceRecognizer.estimate_cosine_similarity(embedding1=embedding1, embedding2=embedding2)
        percent_similarity = self._convert_cosine_to_percent(cosine_value=cosine_similarity)
        return percent_similarity

    def make_image(self, similarity: int = 50, new_width: int = 2200, new_height: int = 450) -> Image:
        image_scale = 0.5 * (similarity + 1) / 100

        # 新しい画像サイズに基づいて左右の画像をリサイズ
        left_image = self._original_image1.convert("RGBA")
        right_image = self._original_image2.convert("RGBA")

        # 縦横比を維持しながらリサイズ
        left_image_ratio = left_image.width / left_image.height
        right_image_ratio = right_image.width / right_image.height

        new_left_width = int(new_height * left_image_ratio)
        new_right_width = int(new_height * right_image_ratio)

        left_image = left_image.resize((new_left_width, new_height))
        right_image = right_image.resize((new_right_width, new_height))

        # 中央の画像をリサイズ
        middle_image = Image.open("./data/heart.png").convert("RGBA")
        draw = ImageDraw.Draw(middle_image)
        font = ImageFont.truetype("arial.ttf", 80)  # FONT_TYPEを適切なフォントパスに置き換えてください
        draw.text((130, 150), f"{similarity}%", fill="black", font=font)

        width, height = middle_image.size
        middle_image = middle_image.resize((int(width * image_scale * 2.5), int(height * image_scale * 2.5)))

        # 新しい画像を作成
        new_image = Image.new("RGBA", (new_width, new_height))

        # 画像を新しい画像に貼り付け
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
