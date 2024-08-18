import cv2

from .result import MatchResult, NoneMatchResult
from .template import Template
from ..algo.generate import OffsetPointGenerator, NoneOffsetPointGenerator
from ..common import Rect, RGB
from ..cv import find_multi_colors
from ..touch import Touch


class MultiColorMatchResult(MatchResult):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y

    def click(self, touch: Touch, duration: int, algorithm: OffsetPointGenerator = NoneOffsetPointGenerator) -> bool:
        x, y = algorithm.generate(self.x, self.y)
        touch.click(x, y, duration)
        return True


class MultiColorTemplate(Template):
    def __init__(self,
                 first_color: str | int | RGB,
                 colors: list[tuple[int, int, int | str | RGB]],
                 region: Rect = None,
                 threshold: int = 4) -> None:
        super().__init__()
        self.first_color = first_color
        self.colors = colors
        self.region = region
        self.threshold = threshold

    def match(self, image: cv2.Mat) -> MultiColorMatchResult | NoneMatchResult:
        result = find_multi_colors(image, self.first_color, self.colors, self.region, self.threshold)
        if result is None:
            return NoneMatchResult()
        return MultiColorMatchResult(result.x, result.y)
