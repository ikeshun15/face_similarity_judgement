class Size:
    def __init__(self, width: int | float, height: int | float) -> None:
        self._width = int(width)
        self._height = int(height)
        self._ratio = width / height

    @classmethod
    def from_tuple(cls, size: tuple[int | float, int | float]) -> "Size":
        return cls(width=size[0], height=size[1])

    @property
    def tuple(self) -> tuple[int, int]:
        return (self._width, self._height)

    @property
    def w(self) -> int:
        return self._width

    @property
    def h(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def ratio(self) -> float:
        return self._ratio
