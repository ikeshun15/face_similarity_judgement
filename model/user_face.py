from insightface.app.common import Face
from insightface.model_zoo.model_zoo import get_model
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class UserFace:
    def __init__(self, image_path1, image_path2):
        self._decoder = get_model('./insight_face_models/models/buffalo_l/det_10g.onnx')
        self._decoder.prepare(ctx_id=0, input_size=(640, 640))
        self._encoder = get_model('./insight_face_models/models/buffalo_l/w600k_r50.onnx')
        self._encoder.prepare(ctx_id=0)

        self._original_image1 = Image.open(image_path1).convert('RGB')
        self._original_image2 = Image.open(image_path2).convert('RGB')

        self._image1 = np.array(self._original_image1)
        self._image2 = np.array(self._original_image2)
    
    def detect_faces(self):
        face_boxes1, kpss1 = self._decoder.detect(img=self._image1)
        face_boxes2, kpss2 = self._decoder.detect(img=self._image2)

        self._detected_face1 = Face(bbox=face_boxes1[0][0:4], kps=kpss1[0])
        self._detected_face2 = Face(bbox=face_boxes2[0][0:4], kps=kpss2[0])

        self._encoder.get(img=self._image1, face=self._detected_face1)
        self._encoder.get(img=self._image2, face=self._detected_face2)

        if self._detected_face1 and self._detected_face2:
            return True
        return False
    
    def estimate_cosine_similarity(self):
        a = np.matmul(self._detected_face1.embedding.T, self._detected_face2.embedding)
        b = np.sum(np.multiply(self._detected_face1.embedding, self._detected_face1.embedding))
        c = np.sum(np.multiply(self._detected_face2.embedding, self._detected_face2.embedding))
        return a / (np.sqrt(b) * np.sqrt(c))

    def make_image(self, scale: float = 0.8, new_height: int = 600) -> Image:
        image_scale = 0.5 * scale + 0.5

        left_image = self._original_image1.convert('RGBA')
        middle_image = Image.open('./data/heart.png').convert('RGBA')
        right_image = self._original_image2.convert('RGBA')

        left_image = left_image.resize((int(left_image.width * new_height / left_image.height), new_height))
        middle_image = middle_image.resize((int(middle_image.width * int(new_height/3) / middle_image.height), int(new_height/3)))
        right_image = right_image.resize((int(right_image.width * new_height / right_image.height), new_height))

        draw = ImageDraw.Draw(middle_image)
        font = ImageFont.truetype('arial.ttf', 50)
        draw.text((55, 65), "{:.3f}".format(scale), fill='black', font=font)

        width, height = middle_image.size
        middle_image = middle_image.resize((int(width*image_scale*2.5), int(height*image_scale*2.5)))

        new_width = max(left_image.width, middle_image.width, right_image.width) * 3
        new_height = max(left_image.height, middle_image.height, right_image.height)

        new_image = Image.new('RGBA', (new_width, new_height))

        new_image.paste(left_image, ((new_width // 3 - left_image.width) // 2, (new_height - left_image.height) // 2))
        new_image.paste(middle_image, ((new_width // 3 - middle_image.width) // 2 + new_width // 3, (new_height - middle_image.height) // 2), middle_image)
        new_image.paste(right_image, ((new_width // 3 - right_image.width) // 2 + new_width * 2 // 3, (new_height - right_image.height) // 2))

        return new_image