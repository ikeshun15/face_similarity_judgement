import os

from dotenv import load_dotenv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .face_recognizer import FaceRecognizer

load_dotenv()


class UserFace:
    def __init__(self, image_path1, image_path2):
        self._face_recognizer = FaceRecognizer()

        self._original_image1 = Image.open(image_path1).convert("RGB")
        self._original_image2 = Image.open(image_path2).convert("RGB")

        self._image1 = np.array(self._original_image1)
        self._image2 = np.array(self._original_image2)

    def estimate_similarity(self) -> float:
        embedding1 = self._face_recognizer.detect_and_encode_face(image=self._image1)
        embedding2 = self._face_recognizer.detect_and_encode_face(image=self._image2)

        assert type(embedding1) == np.ndarray
        assert type(embedding2) == np.ndarray

        cosine_similarity = FaceRecognizer.estimate_cosine_similarity(embedding1=embedding1, embedding2=embedding2)
        return cosine_similarity

    def make_image(self, scale: float = 0.8, new_height: int = 600) -> Image:
        image_scale = 0.5 * scale + 0.5

        left_image = self._original_image1.convert("RGBA")
        middle_image = Image.open("./data/heart.png").convert("RGBA")
        right_image = self._original_image2.convert("RGBA")

        left_image = left_image.resize((int(left_image.width * new_height / left_image.height), new_height))
        middle_image = middle_image.resize((int(middle_image.width * int(new_height / 3) / middle_image.height), int(new_height / 3)))
        right_image = right_image.resize((int(right_image.width * new_height / right_image.height), new_height))

        draw = ImageDraw.Draw(middle_image)
        font = ImageFont.truetype(os.environ["IMAGE_FONT"], 50)
        draw.text((55, 65), "{:.3f}".format(scale), fill="black", font=font)

        width, height = middle_image.size
        middle_image = middle_image.resize((int(width * image_scale * 2.5), int(height * image_scale * 2.5)))

        new_width = max(left_image.width, middle_image.width, right_image.width) * 3
        new_height = max(left_image.height, middle_image.height, right_image.height)

        new_image = Image.new("RGBA", (new_width, new_height))

        new_image.paste(left_image, ((new_width // 3 - left_image.width) // 2, (new_height - left_image.height) // 2))
        new_image.paste(middle_image, ((new_width // 3 - middle_image.width) // 2 + new_width // 3, (new_height - middle_image.height) // 2), middle_image)
        new_image.paste(right_image, ((new_width // 3 - right_image.width) // 2 + new_width * 2 // 3, (new_height - right_image.height) // 2))

        return new_image
