import numpy as np


class BBox:
    def __init__(self, x0: int, x1: int, y0: int, y1: int):
        self._x0 = x0
        self._x1 = x1
        self._y0 = y0
        self._y1 = y1

    @classmethod
    def from_array(cls, bbox: np.ndarray) -> "BBox":
        assert bbox.shape == (4,)
        x0, y0, x1, y1 = bbox.astype(int)
        return cls(x0=x0, x1=x1, y0=y0, y1=y1)

    @property
    def x0(self) -> int:
        return self._x0

    @property
    def x1(self) -> int:
        return self._x1

    @property
    def y0(self) -> int:
        return self._y0

    @property
    def y1(self) -> int:
        return self._y1

    @property
    def x(self) -> int:
        return self._x1 - self._x0

    @property
    def y(self) -> int:
        return self._y1 - self._y0

    @property
    def cx(self) -> int:
        return (self._x0 + self._x1) // 2

    @property
    def cy(self) -> int:
        return (self._y0 + self._y1) // 2

    def copy(self) -> "BBox":
        return BBox(x0=self.x0, x1=self.x1, y0=self.y0, y1=self.y1)

    def move(self, dx: int = 0, dy: int = 0) -> "BBox":
        return BBox(x0=self.x0 + dx, x1=self.x1 + dx, y0=self.y0 + dy, y1=self.y1 + dy)
