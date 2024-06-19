import numpy as np
import cv2
from PIL import Image

from .bbox import BBox
from .face_recognizer import FaceRecognizerFactory
from .user_faces import UserFaces


class SimilarityAnalyzer:
    def __init__(self, image_rgb_1: Image.Image, image_rgb_2: Image.Image) -> None:
        self._np_image_rgb_1 = np.array(image_rgb_1, dtype=np.uint8)
        self._np_image_rgb_2 = np.array(image_rgb_2, dtype=np.uint8)

    def analyze(self) -> Image.Image:
        image_rgb_1, image_rgb_2, percent_similarity = self._estimate_trimed_images_and_percent_similarity()
        user_faces = UserFaces(image_rgb_1=image_rgb_1, image_rgb_2=image_rgb_2)
        conbined_image = user_faces.generate_conbined_image(percent_similarity=percent_similarity)
        return conbined_image

    def _estimate_trimed_images_and_percent_similarity(self) -> tuple[Image.Image, Image.Image, int]:
        face_recognizer = FaceRecognizerFactory.create_as_singleton()

        bbox_array1, embedding1 = face_recognizer.detect_and_encode_face(image_rgb=self._np_image_rgb_1)
        bbox_array2, embedding2 = face_recognizer.detect_and_encode_face(image_rgb=self._np_image_rgb_2)

        trim_bbox1 = self._estimate_trim_bbox(image0=self._np_image_rgb_1, bbox0=BBox.from_array(bbox=bbox_array1))
        trim_bbox2 = self._estimate_trim_bbox(image0=self._np_image_rgb_2, bbox0=BBox.from_array(bbox=bbox_array2))

        image_rgb_1 = self._trim_and_resize_and_convert_image(image=self._np_image_rgb_1, bbox=trim_bbox1)
        image_rgb_2 = self._trim_and_resize_and_convert_image(image=self._np_image_rgb_2, bbox=trim_bbox2)

        cosine_similarity = face_recognizer.estimate_cosine_similarity(embedding1=embedding1, embedding2=embedding2)
        percent_similarity = self._convert_cosine_to_percent(cosine_value=cosine_similarity)

        return image_rgb_1, image_rgb_2, percent_similarity

    @staticmethod
    def _convert_cosine_to_percent(cosine_value: float) -> int:
        percent_value = int((abs(cosine_value) ** (2 / 3)) * 150 + 30)
        if percent_value > 100:
            percent_value = 100
        if percent_value < 0:
            percent_value = 0
        return percent_value

    @staticmethod
    def _estimate_trim_bbox(image0: np.ndarray, bbox0: BBox, factor: float = 2.75):
        y_max, x_max = image0.shape[:2]

        l_want = int(max(bbox0.x, bbox0.y) * factor)
        l_possible = min(x_max, y_max)
        l = min(l_want, l_possible)

        bbox1 = BBox(x0=bbox0.cx - l // 2, y0=bbox0.cy - l // 2, x1=bbox0.cx + l // 2, y1=bbox0.cy + l // 2)

        if bbox1.x0 < 0:
            bbox2 = bbox1.move(dx=-bbox1.x0)
        elif bbox1.x1 > x_max:
            bbox2 = bbox1.move(dx=-(bbox1.x1 - x_max))
        else:
            bbox2 = bbox1.copy()

        if bbox2.y0 < 0:
            bbox3 = bbox2.move(dy=-bbox2.y0)
        elif bbox2.y1 > y_max:
            bbox3 = bbox2.move(dy=-(bbox2.y1 - y_max))
        else:
            bbox3 = bbox2.copy()

        return bbox3

    @staticmethod
    def _trim_and_resize_and_convert_image(image: np.ndarray, bbox: BBox) -> Image.Image:
        trimed_image = image[bbox.y0 : bbox.y1, bbox.x0 : bbox.x1]
        resized_image = cv2.resize(src=trimed_image, dsize=(500, 500))
        return Image.fromarray(resized_image, "RGB")
