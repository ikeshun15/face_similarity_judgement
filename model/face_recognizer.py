import os
import threading

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

    def detect_and_encode_face(self, image_rgb: np.ndarray) -> np.ndarray | None:
        face_boxes, kpss = self._detector.detect(img=image_rgb)

        try:
            assert type(kpss) == np.ndarray
            assert len(face_boxes) == 1
            face = Face(bbox=face_boxes[0][0:4], kps=kpss[0])
        except:
            return None

        return self._encoder.get(img=image_rgb, face=face)

    @staticmethod
    def estimate_cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        a = np.matmul(embedding1.T, embedding2)
        b = np.sum(np.multiply(embedding1, embedding1))
        c = np.sum(np.multiply(embedding2, embedding2))
        return a / (np.sqrt(b) * np.sqrt(c))


class FaceRecognizerFactory:
    _face_recognizer = None
    _lock = threading.Lock()

    @classmethod
    def create_as_singleton(cls) -> FaceRecognizer:
        with cls._lock:
            if cls._face_recognizer is None:
                cls._face_recognizer = FaceRecognizer()
        return cls._face_recognizer
