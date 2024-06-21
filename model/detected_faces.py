import cv2
import numpy as np
from PIL import Image

from .bbox import BBox
from .face_recognizer import FaceRecognizerFactory


class DetectedFaces:
    def __init__(self, image_rgb: np.ndarray, faces: list[tuple[np.ndarray, np.ndarray]]) -> None:
        self._image_rgb = image_rgb
        self._faces = faces

    @classmethod
    def detect(cls, image_rgb: Image.Image) -> "DetectedFaces":
        np_image_rgb = np.array(image_rgb, dtype=np.uint8)
        face_recognizer = FaceRecognizerFactory.create_as_singleton()
        faces = face_recognizer.detect_faces(image_rgb=np_image_rgb)
        return cls(image_rgb=np_image_rgb, faces=faces)

    @property
    def n_faces(self) -> int:
        return len(self._faces)

    @property
    def image_rgb(self) -> np.ndarray:
        return self._image_rgb

    def get_face(self, n: int) -> tuple[np.ndarray, np.ndarray]:
        assert n < self.n_faces
        return self._faces[n]

    def get_face_image(self, n: int, trim_factor: float = 1.0, dsize: tuple[int, int] | None = None) -> Image.Image:
        bbox, _ = self.get_face(n=n)
        trim_bbox = self._estimate_square_trim_bbox(image0=self._image_rgb, bbox0=BBox.from_array(bbox=bbox), factor=trim_factor)
        trimed_image_rgb = self._trim_and_convert_image(image=self._image_rgb, bbox=trim_bbox, dsize=dsize)
        return trimed_image_rgb

    @staticmethod
    def _estimate_square_trim_bbox(image0: np.ndarray, bbox0: BBox, factor: float = 1.0):
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
    def _trim_and_convert_image(image: np.ndarray, bbox: BBox, dsize: tuple[int, int] | None) -> Image.Image:
        trimed_image = image[bbox.y0 : bbox.y1, bbox.x0 : bbox.x1]
        if dsize is not None:
            trimed_image = cv2.resize(src=trimed_image, dsize=dsize)
        return Image.fromarray(trimed_image, "RGB")
