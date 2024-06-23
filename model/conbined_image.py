from PIL import Image, ImageDraw, ImageFont

from .size import Size


FONT_PATH = "./data/DejaVuSans.ttf"
HEART_IMAGE_PATH = "./data/heart.png"
LOGO_IMAGE_PATH = "./data/logo.png"


class ConbinedImage:
    def __init__(
        self,
        image_rgb_1: Image.Image,
        image_rgb_2: Image.Image,
        percent_value: int,
        image_size: tuple[int, int] = (1300, 500),
        image_ratios: tuple[int, int, int] = (5, 3, 5),
        margin: int = 80,
        bg_color: str = "#FFFFFF",
        text_color: str = "#000000",
        logo_text: str = "ABCDEFG",
    ) -> None:
        max_size = Size.from_tuple(size=image_size)
        max_size_l = Size(width=max_size.w * image_ratios[0] / sum(image_ratios), height=max_size.h)
        max_size_r = Size(width=max_size.w * image_ratios[2] / sum(image_ratios), height=max_size.h)
        max_size_m = Size(width=max_size.w * image_ratios[1] / sum(image_ratios), height=max_size.h)
        middle_image_factor = (percent_value / 100) * 2 / 3 + 1 / 3
        size_m = Size(width=max_size_m.w * middle_image_factor, height=max_size_m.h * middle_image_factor)
        max_size_logo = Size(max_size.w, margin // 2)

        image_rgba_1 = image_rgb_1.convert(mode="RGBA")
        image_rgba_2 = image_rgb_2.convert(mode="RGBA")
        heart_image_rgba = self._get_heart_image(percent_value=percent_value, text_color=bg_color)
        logo_icon_image_rgba = self._get_logo_image()
        logo_text_image_rgba = self._get_text_image(text=logo_text, text_color=text_color)

        left_image = self._resize(image=image_rgba_1, max_size=max_size_l)
        right_image = self._resize(image=image_rgba_2, max_size=max_size_r)
        middle_image = self._resize(image=heart_image_rgba, max_size=size_m)
        logo_icon_image = self._resize(image=logo_icon_image_rgba, max_size=max_size_logo, margin=margin // 5)
        logo_text_image = self._resize(image=logo_text_image_rgba, max_size=max_size_logo, margin=margin // 5)

        pasted_image = Image.new(mode="RGBA", size=max_size.tuple)
        pasted_image.paste(
            im=left_image,
            box=((max_size_l.w - left_image.width) // 2, (max_size_l.h - left_image.height) // 2),
        )
        pasted_image.paste(
            im=middle_image,
            box=((max_size_m.w - middle_image.width) // 2 + max_size_l.w, (max_size_m.h - middle_image.height) // 2),
        )
        pasted_image.paste(
            im=right_image,
            box=((max_size_r.w - right_image.width) // 2 + max_size_l.w + max_size_m.w, (max_size_r.h - right_image.height) // 2),
        )
        pasted_image = self._resize(image=pasted_image, max_size=max_size, margin=margin)

        conbined_image = Image.new(mode="RGBA", size=max_size.tuple, color=bg_color)
        conbined_image.paste(im=pasted_image, box=(margin // 2, margin // 2))
        conbined_image.paste(im=logo_icon_image, box=(margin // 2, max_size.h - margin // 2 + margin // 10))
        conbined_image.paste(im=logo_text_image, box=(margin // 2 + logo_icon_image.width, max_size.h - margin // 2 + margin // 10))
        self._image = conbined_image

    @property
    def image(self) -> Image.Image:
        return self._image

    @staticmethod
    def _resize(image: Image.Image, max_size: Size, margin: int = 0) -> Image.Image:
        true_max_size = Size(width=max_size.w - margin, height=max_size.h - margin)
        image_size = Size(width=image.width, height=image.height)
        ideal_width = int(true_max_size.h * image_size.ratio)

        if ideal_width <= true_max_size.w:
            new_image_size = Size(width=ideal_width, height=true_max_size.h)
        else:
            new_image_size = Size(width=true_max_size.w, height=true_max_size.h * true_max_size.w / ideal_width)

        resized_image = image.resize(size=new_image_size.tuple)
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
    def _get_logo_image() -> Image.Image:
        logo_image = Image.open(fp=LOGO_IMAGE_PATH).convert(mode="RGBA")
        return logo_image

    @staticmethod
    def _get_text_image(text: str, text_color: str) -> Image.Image:
        text_image = Image.new(mode="RGBA", size=(2000, 90))
        draw = ImageDraw.Draw(im=text_image)
        font = ImageFont.truetype(font=FONT_PATH, size=80)
        draw.text(xy=(1, 5), text=text, fill=text_color, font=font)
        return text_image
