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
                 colors: list[tuple[int | str | RGB]],
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

    @staticmethod
    def from_dict(data: dict):
        first_color = data.get('first_color')
        if not isinstance(first_color, (str, int, RGB)):
            raise TypeError("first_color must be str, int or RGB")

        colors: list[tuple[int, int, int | str | RGB]] = data.get('colors')
        if colors is None:
            raise ValueError("colors must be exists")
        if not isinstance(colors, list) and not isinstance(colors, tuple):
            raise TypeError("colors must be list or tuple")
        if any(len(color) !=3 for color in colors):
            raise ValueError("colors must be list or tuple of (x,y,color)")
        if any(not isinstance(color[0],int) or not isinstance(color[1],int) or not isinstance(color[2],(str,int,RGB))  for color in colors):
            raise TypeError("(x,y,color) must be (int, int, str or int or RGB)")

        tmp_region: list[int] | tuple[int] | Rect | None = data.get('region', None)
        if isinstance(tmp_region, (list, tuple)):
            region = Rect(tmp_region[0], tmp_region[1], tmp_region[2], tmp_region[3])
        elif isinstance(tmp_region, Rect):
            region = tmp_region
        elif tmp_region is None:
            region = None
        else:
            raise TypeError("region must be list, tuple or Rect")

        threshold = data.get('threshold', 4)
        if threshold < 0 or threshold > 255:
            raise ValueError("threshold must be between 0 and 255")

        return MultiColorTemplate(first_color, colors, region, threshold)
