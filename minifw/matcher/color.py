import cv2

from minifw.common import Rect, RGB
from minifw.cv import find_multi_colors
from minifw.matcher.result import NoneMatchResult, PointMatchResult
from minifw.matcher.template import Template


class MultiColorTemplate(Template):

    def __str__(self) -> str:
        return f"MultiColorTemplate({self.first_color}, {self.colors}, {self.region}, {self.threshold})"

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

    def match(self, image: cv2.Mat) -> PointMatchResult | NoneMatchResult:
        result = find_multi_colors(image, self.first_color, self.colors, self.region, self.threshold)
        if result is None:
            return NoneMatchResult()
        return PointMatchResult(result.x, result.y)
