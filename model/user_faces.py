from PIL import Image, ImageDraw, ImageFont

from .settting import Setting


class UserFaces:
    def __init__(self, image_rgb_1: Image.Image, image_rgb_2: Image.Image) -> None:
        self._image_rgb_1 = image_rgb_1
        self._image_rgb_2 = image_rgb_2

    def generate_conbined_image(self, percent_similarity: int = 50, new_width: int = 1500, new_height: int = 500) -> Image.Image:
        image_scale = 0.4 * (percent_similarity + 1) / 100

        left_image = self._image_rgb_1.convert("RGBA")
        right_image = self._image_rgb_2.convert("RGBA")

        left_image_ratio = left_image.width / left_image.height
        right_image_ratio = right_image.width / right_image.height

        new_left_width = int(new_height * left_image_ratio)
        new_right_width = int(new_height * right_image_ratio)

        left_image = left_image.resize((new_left_width, new_height))
        right_image = right_image.resize((new_right_width, new_height))

        middle_image = Image.open(Setting.HEART_IMAGE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(middle_image)
        font = ImageFont.truetype(Setting.FONT_TYPE, 80)
        draw.text((130, 150), f"{percent_similarity}%", fill="black", font=font)

        width, height = middle_image.size
        middle_image = middle_image.resize((int(width * image_scale * 2.5), int(height * image_scale * 2.5)))

        conbined_image = Image.new("RGBA", (new_width, new_height))

        conbined_image.paste(left_image, ((new_width // 3 - new_left_width) // 2, (new_height - left_image.height) // 2))
        conbined_image.paste(middle_image, ((new_width // 3 - middle_image.width) // 2 + new_width // 3, (new_height - middle_image.height) // 2), middle_image)
        conbined_image.paste(right_image, ((new_width // 3 - new_right_width) // 2 + new_width * 2 // 3, (new_height - right_image.height) // 2))

        return conbined_image
