from PIL import Image, ImageDraw, ImageFont

from .settting import Setting


class UserFaces:
    def __init__(self, image_rgb_1: Image.Image, image_rgb_2: Image.Image) -> None:
        self._image_rgba_1 = image_rgb_1.convert("RGBA")
        self._image_rgba_2 = image_rgb_2.convert("RGBA")

    def generate_conbined_image(self, percent_value: int = 50, image_size: tuple[int, int] = (1300, 500), image_ratios: tuple[int, int, int] = (5, 3, 5)) -> Image.Image:
        conbined_image = Image.new("RGBA", image_size)
        middle_image_factor = percent_value / 200 + 0.5

        max_size_l = (int(image_size[0] * image_ratios[0] / sum(image_ratios)), image_size[1])
        max_size_r = (int(image_size[0] * image_ratios[2] / sum(image_ratios)), image_size[1])
        max_size_m = (int(image_size[0] * image_ratios[1] / sum(image_ratios)), image_size[1])

        left_image = self._resize(image=self._image_rgba_1, max_size=max_size_l)
        right_image = self._resize(image=self._image_rgba_2, max_size=max_size_r)
        heart_image_rgba = self._get_heart_image(percent_value=percent_value)
        middle_image = self._resize(image=heart_image_rgba, max_size=max_size_m)
        middle_image = middle_image.resize((int(middle_image.width * middle_image_factor), int(middle_image.height * middle_image_factor)))

        conbined_image.paste(left_image, ((max_size_l[0] - left_image.width) // 2, (max_size_l[1] - left_image.height) // 2))
        conbined_image.paste(middle_image, ((max_size_m[0] - middle_image.width) // 2 + max_size_l[0], (max_size_m[1] - middle_image.height) // 2), middle_image)
        conbined_image.paste(right_image, ((max_size_r[0] - right_image.width) // 2 + max_size_l[0] + max_size_m[0], (max_size_r[1] - right_image.height) // 2))

        return conbined_image

    @staticmethod
    def _resize(image: Image.Image, max_size: tuple[int, int]) -> Image.Image:
        max_width, max_height = max_size

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
    def _get_heart_image(percent_value: int) -> Image.Image:
        heart_image = Image.open(Setting.HEART_IMAGE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(heart_image)
        font = ImageFont.truetype(Setting.FONT_TYPE, 80)
        draw.text((130, 150), f"{percent_value}%", fill="black", font=font)
        return heart_image
