from PIL import Image, ImageDraw, ImageFont

from .face_recognizer import FaceRecognizerFactory
from .detected_faces import DetectedFaces


FONT_PATH = "./data/DejaVuSans.ttf"
HEART_IMAGE_PATH = "./data/heart.png"


class ConbinedImage:
    def __init__(
        self,
        image_rgb_1: Image.Image,
        image_rgb_2: Image.Image,
        percent_value: int,
        image_size: tuple[int, int] = (1300, 500),
        image_ratios: tuple[int, int, int] = (5, 3, 5),
        margin: int = 80,
        bg_color: str = "#FDF9DA",
        text_color: str = "#8B3626",
    ) -> None:
        max_size_l = (int(image_size[0] * image_ratios[0] / sum(image_ratios)), image_size[1])
        max_size_r = (int(image_size[0] * image_ratios[2] / sum(image_ratios)), image_size[1])
        max_size_m = (int(image_size[0] * image_ratios[1] / sum(image_ratios)), image_size[1])

        image_rgba_1 = image_rgb_1.convert(mode="RGBA")
        image_rgba_2 = image_rgb_2.convert(mode="RGBA")
        heart_image_rgba = self._get_heart_image(percent_value=percent_value, text_color=bg_color)
        text_image_rgba = self._get_text_image(text=f"Created with #DoWeLookAlike?", text_color=text_color)

        left_image = self._resize(image=image_rgba_1, max_size=max_size_l)
        right_image = self._resize(image=image_rgba_2, max_size=max_size_r)
        middle_image = self._resize(image=heart_image_rgba, max_size=max_size_m)
        middle_image_factor = percent_value / 200 + 0.5
        middle_image = middle_image.resize((int(middle_image.width * middle_image_factor), int(middle_image.height * middle_image_factor)))
        logo_image = self._resize(image=text_image_rgba, max_size=(image_size[0], margin // 2), margin=margin // 10)

        pasted_image = Image.new(mode="RGBA", size=image_size)
        pasted_image.paste(im=left_image, box=((max_size_l[0] - left_image.width) // 2, (max_size_l[1] - left_image.height) // 2))
        pasted_image.paste(im=middle_image, box=((max_size_m[0] - middle_image.width) // 2 + max_size_l[0], (max_size_m[1] - middle_image.height) // 2))
        pasted_image.paste(im=right_image, box=((max_size_r[0] - right_image.width) // 2 + max_size_l[0] + max_size_m[0], (max_size_r[1] - right_image.height) // 2))
        pasted_image = self._resize(image=pasted_image, max_size=image_size, margin=margin)

        conbined_image = Image.new(mode="RGBA", size=image_size, color=bg_color)
        conbined_image.paste(im=pasted_image, box=(margin // 2, margin // 2))
        conbined_image.paste(im=logo_image, box=(margin // 2, image_size[1] - margin // 2))
        self._image = conbined_image

    @property
    def image(self) -> Image.Image:
        return self._image

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
        heart_image = Image.open(fp=HEART_IMAGE_PATH).convert(mode="RGBA")
        draw = ImageDraw.Draw(im=heart_image)
        font = ImageFont.truetype(font=FONT_PATH, size=80)
        if percent_value == 100:
            x = 140
        elif percent_value < 10:
            x = 180
        else:
            x = 160
        draw.text(xy=(x, 200), text=f"{percent_value}%", fill=text_color, font=font)
        return heart_image

    @staticmethod
    def _get_text_image(text: str, text_color: str) -> Image.Image:
        text_image = Image.new(mode="RGBA", size=(2000, 120))
        draw = ImageDraw.Draw(im=text_image)
        font = ImageFont.truetype(font=FONT_PATH, size=80)
        draw.text(xy=(1, 1), text=text, fill=text_color, font=font)
        return text_image
