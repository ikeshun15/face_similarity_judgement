import numpy as np

from insightface.app import FaceAnalysis
from insightface.app.common import Face
from insightface.model_zoo.model_zoo import get_model, RetinaFace, ArcFaceONNX


ROOT_DIR_PATH = "./insight_face_models/"
DETECTOR_PATH = ROOT_DIR_PATH + "models/buffalo_l/det_10g.onnx"
ENCODER_PATH = ROOT_DIR_PATH + "models/buffalo_l/w600k_r50.onnx"


class FaceRecognizer:
    def __init__(self):
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
            face = Face(bbox=face_boxes[0][0:4], kps=kpss[0])
        except:
            return None

        return self._encoder.get(img=image, face=face)

    @staticmethod
    def download_model(model_name: str = "buffalo_l"):
        FaceAnalysis(name=model_name, root=ROOT_DIR_PATH)
