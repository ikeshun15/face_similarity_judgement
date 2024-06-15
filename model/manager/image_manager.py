from PIL import Image

class ImageManager:
    @staticmethod
    def make_image(image1_path: str, image2_path: str, scale: int = 0.8) -> Image:
        # 画像を読み込む
        image1 = Image.open(image1_path).convert("RGBA")
        heart = Image.open('./data/heart.png').convert("RGBA")
        image2 = Image.open(image2_path).convert("RGBA")

        images = [image1, heart, image2]

        # 最大の幅と高さを取得
        max_width = max(image.size[0] for image in images)
        max_height = max(image.size[1] for image in images)

        # 各画像の幅と高さを最大の幅と高さに揃える
        for i in range(len(images)):
            if i == 1:  # image2のみ拡大縮小を行う
                scaled_width = int(images[i].size[0] * scale)
                scaled_height = int(images[i].size[1] * scale)
                images[i] = images[i].resize((scaled_width, scaled_height))

            new_image = Image.new('RGBA', (max_width, max_height))
            offset = ((max_width - images[i].size[0]) // 2, (max_height - images[i].size[1]) // 2)
            new_image.paste(images[i], offset)
            images[i] = new_image

        # 画像を横に連結
        image = Image.new('RGBA', (max_width * len(images), max_height))
        for i in range(len(images)):
            image.paste(images[i], (i * max_width, 0))

        return image