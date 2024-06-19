import numpy as np
from PIL import Image

from .face_recognizer import FaceRecognizerFactory
from .user_faces import UserFaces


class SimilarityAnalyzer:
    def __init__(self, image_rgb_1: Image.Image, image_rgb_2: Image.Image) -> None:
        self._user_faces = UserFaces(image_rgb_1=image_rgb_1, image_rgb_2=image_rgb_2)
        self._face_recognizer = FaceRecognizerFactory.create_as_singleton()

    def analyze(self) -> Image.Image:
        percent_similarity = self._estimate_percent_similarity()
        conbined_image = self._user_faces.generate_conbined_image(percent_similarity=percent_similarity)
        return conbined_image

    def _estimate_percent_similarity(self) -> int:
        np_image_rgb_1 = np.array(self._user_faces.image_rgb_1)
        np_image_rgb_2 = np.array(self._user_faces.image_rgb_2)

        embedding1 = self._face_recognizer.detect_and_encode_face(image_rgb=np_image_rgb_1)
        embedding2 = self._face_recognizer.detect_and_encode_face(image_rgb=np_image_rgb_2)

        assert type(embedding1) == np.ndarray
        assert type(embedding2) == np.ndarray

        cosine_similarity = self._face_recognizer.estimate_cosine_similarity(embedding1=embedding1, embedding2=embedding2)
        percent_similarity = self._convert_cosine_to_percent(cosine_value=cosine_similarity)

        return percent_similarity

    @staticmethod
    def _convert_cosine_to_percent(cosine_value: float) -> int:
        percent_value = int((abs(cosine_value) ** (2 / 3)) * 150 + 30)
        if percent_value > 100:
            percent_value = 100
        if percent_value < 0:
            percent_value = 0
        return percent_value
