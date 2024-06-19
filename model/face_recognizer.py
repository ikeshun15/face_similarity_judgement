import os
import threading

import numpy as np
from insightface.app import FaceAnalysis
from insightface.app.common import Face
from insightface.model_zoo.model_zoo import get_model, RetinaFace, ArcFaceONNX


ROOT_DIR_PATH = "./insight_face_models/"
DETECTOR_PATH = ROOT_DIR_PATH + "models/buffalo_l/det_10g.onnx"
ENCODER_PATH = ROOT_DIR_PATH + "models/buffalo_l/w600k_r50.onnx"


class FaceRecognizer:
    def __init__(self) -> None:
        detector = get_model(DETECTOR_PATH)
        assert type(detector) == RetinaFace
        detector.prepare(ctx_id=0, input_size=(640, 640))

        encoder = get_model(ENCODER_PATH)
        assert type(encoder) == ArcFaceONNX
        encoder.prepare(ctx_id=0)

        self._detector = detector
        self._encoder = encoder

    def detect_and_encode_face(self, image: np.ndarray) -> np.ndarray | None:
        face_boxes, kpss = self._detector.detect(img=image)

        try:
            assert type(kpss) == np.ndarray
            assert len(face_boxes) == 1
            face = Face(bbox=face_boxes[0][0:4], kps=kpss[0])
        except:
            return None

        return self._encoder.get(img=image, face=face)

    @staticmethod
    def estimate_cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        a = np.matmul(embedding1.T, embedding2)
        b = np.sum(np.multiply(embedding1, embedding1))
        c = np.sum(np.multiply(embedding2, embedding2))
        return a / (np.sqrt(b) * np.sqrt(c))


class FaceRecognizerFactory:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def download_model_if_not_exists(model_name: str = "buffalo_l") -> None:
        if not os.path.isdir(s=ROOT_DIR_PATH):
            FaceAnalysis(name=model_name, root=ROOT_DIR_PATH)

    @classmethod
    def create_as_singleton(cls) -> FaceRecognizer:
        with cls._lock:
            if cls._instance is None:
                cls._instance = FaceRecognizer()
        return cls._instance
