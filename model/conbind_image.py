from PIL import Image, ImageDraw, ImageFont

from .settting import Setting
from .face_recognizer import FaceRecognizerFactory
from .detected_faces import DetectedFaces


class ConbindedImage:
    def __init__(
        self,
        image_rgb_1: Image.Image,
        image_rgb_2: Image.Image,
        percent_value: int,
        image_size: tuple[int, int] = (1300, 500),
        image_ratios: tuple[int, int, int] = (5, 3, 5),
        margin: int = 80,
        background_color: str = "#FDF9DA",
        text_color: str = "#8B3626",
    ) -> None:
        image_rgba_1 = image_rgb_1.convert("RGBA")
        image_rgba_2 = image_rgb_2.convert("RGBA")

        conbined_image = Image.new("RGBA", image_size, color=background_color)
        draw = ImageDraw.Draw(conbined_image)
        font = ImageFont.truetype(Setting.FONT_TYPE, 20)
        x0 = int(image_size[0] - 280 - margin)
        y0 = int(image_size[1] - margin / 2.5)
        draw.text((x0, y0), f"Created with #DoWeLookAlike?", fill=text_color, font=font)

        middle_image_factor = percent_value / 200 + 0.5

        max_size_l = (int(image_size[0] * image_ratios[0] / sum(image_ratios)), image_size[1])
        max_size_r = (int(image_size[0] * image_ratios[2] / sum(image_ratios)), image_size[1])
        max_size_m = (int(image_size[0] * image_ratios[1] / sum(image_ratios)), image_size[1])

        left_image = self._resize(image=image_rgba_1, max_size=max_size_l, margin=margin)
        right_image = self._resize(image=image_rgba_2, max_size=max_size_r, margin=margin)
        heart_image_rgba = self._get_heart_image(percent_value=percent_value, text_color=background_color)
        middle_image = self._resize(image=heart_image_rgba, max_size=max_size_m)
        middle_image = middle_image.resize((int(middle_image.width * middle_image_factor), int(middle_image.height * middle_image_factor)))

        conbined_image.paste(left_image, ((max_size_l[0] - left_image.width) // 2, (max_size_l[1] - left_image.height) // 2))
        conbined_image.paste(middle_image, ((max_size_m[0] - middle_image.width) // 2 + max_size_l[0], (max_size_m[1] - middle_image.height) // 2), middle_image)
        conbined_image.paste(right_image, ((max_size_r[0] - right_image.width) // 2 + max_size_l[0] + max_size_m[0], (max_size_r[1] - right_image.height) // 2))

        self._image = conbined_image

    @classmethod
    def based_similarity(
        cls,
        detected_faces1: DetectedFaces,
        n_selected1: int,
        detected_faces2: DetectedFaces,
        n_selected2: int,
    ) -> "ConbindedImage":
        face1 = detected_faces1.get_face(n=n_selected1)
        face2 = detected_faces2.get_face(n=n_selected2)
        image_rgb_1 = detected_faces1.get_face_image(n=n_selected1, trim_factor=2.0, dsize=(500, 500))
        image_rgb_2 = detected_faces2.get_face_image(n=n_selected2, trim_factor=2.0, dsize=(500, 500))
        face_recognizer = FaceRecognizerFactory.create_as_singleton()
        cosine_similarity = face_recognizer.encode_faces_and_estimate_cosine_similarity(
            image_rgb1=detected_faces1.image_rgb, face1=face1, image_rgb2=detected_faces2.image_rgb, face2=face2
        )
        percent_similarity = cls._convert_cosine_to_percent(cosine_value=cosine_similarity)
        return cls(
            image_rgb_1=image_rgb_1,
            image_rgb_2=image_rgb_2,
            percent_value=percent_similarity,
        )

    @property
    def image(self) -> Image.Image:
        return self._image

    @staticmethod
    def _convert_cosine_to_percent(cosine_value: float) -> int:
        percent_value = int((abs(cosine_value) ** (2 / 3)) * 150 + 30)
        if percent_value > 100:
            percent_value = 100
        if percent_value < 0:
            percent_value = 0
        return percent_value

    @staticmethod
    def _resize(image: Image.Image, max_size: tuple[int, int], margin: int = 0) -> Image.Image:
        max_width, max_height = max_size
        max_width -= margin
        max_height -= margin

        image_ratio = image.width / image.height
        ideal_width = int(max_height * image_ratio)

        if ideal_width <= max_width:
            new_width = ideal_width
            new_height = max_height
        else:
            new_width = max_width
            new_height = int(max_height * max_width / ideal_width)

        resized_image = image.resize((new_width, new_height))
        return resized_image

    @staticmethod
    def _get_heart_image(percent_value: int, text_color: str) -> Image.Image:
        heart_image = Image.open(Setting.HEART_IMAGE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(heart_image)
        font = ImageFont.truetype(Setting.FONT_TYPE, 80)
        draw.text((130, 150), f"{percent_value}%", fill=text_color, font=font)
        return heart_image
