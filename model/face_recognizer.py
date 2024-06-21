import os

import numpy as np
from insightface.app import FaceAnalysis
from insightface.app.common import Face
from insightface.model_zoo.model_zoo import get_model, RetinaFace, ArcFaceONNX

from .settting import Setting


def download_model_if_not_exists() -> None:
    if not os.path.isdir(s=Setting.ROOT_DIR_PATH):
        FaceAnalysis(name=Setting.MODEL_NAME, root=Setting.ROOT_DIR_PATH)


class FaceRecognizer:
    def __init__(self) -> None:
        detector = get_model(Setting.DETECTOR_PATH)
        assert type(detector) == RetinaFace
        detector.prepare(ctx_id=0, input_size=(640, 640))

        encoder = get_model(Setting.ENCODER_PATH)
        assert type(encoder) == ArcFaceONNX
        encoder.prepare(ctx_id=0)

        self._detector = detector
        self._encoder = encoder

    def detect_faces(self, image_rgb: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
        bboxes, kpses = self._detector.detect(img=image_rgb)
        assert type(kpses) == np.ndarray
        assert len(bboxes) == len(kpses)
        return [(bbox[0:4], kps) for bbox, kps in zip(bboxes, kpses)]

    def encode_faces(self, image_rgb: np.ndarray, faces: list[tuple[np.ndarray, np.ndarray]]) -> list[np.ndarray]:
        embeddings: list[np.ndarray] = []
        for bbox, kps in faces:
            face = Face(bbox=bbox, kps=kps)
            embedding = self._encoder.get(img=image_rgb, face=face)
            assert type(embedding) == np.ndarray
            embeddings.append(embedding)
        return embeddings

    @staticmethod
    def estimate_cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        a = np.matmul(embedding1.T, embedding2)
        b = np.sum(np.multiply(embedding1, embedding1))
        c = np.sum(np.multiply(embedding2, embedding2))
        return a / (np.sqrt(b) * np.sqrt(c))

    def encode_faces_and_estimate_cosine_similarity(self, image_rgb: np.ndarray, face1: tuple[np.ndarray, np.ndarray], face2: tuple[np.ndarray, np.ndarray]) -> float:
        embedding1, embedding2 = self.encode_faces(image_rgb=image_rgb, faces=[face1, face2])
        cosine_similarity = self.estimate_cosine_similarity(embedding1=embedding1, embedding2=embedding2)
        return cosine_similarity


class FaceRecognizerFactory:
    _face_recognizer = None

    @classmethod
    def create_as_singleton(cls) -> FaceRecognizer:
        if cls._face_recognizer is None:
            cls._face_recognizer = FaceRecognizer()
        return cls._face_recognizer
