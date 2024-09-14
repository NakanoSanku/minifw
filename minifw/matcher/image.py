import os
import cv2

from minifw.common import Rect
from minifw.cv import match_template_best, imread, get_height, get_width
from minifw.matcher.result import NoneMatchResult, RectMatchResult
from minifw.matcher.template import Template


class ImageTemplate(Template):
    def __str__(self) -> str:
        return f"ImageTemplate(template_path={self.template_path}, region={self.region}, threshold={self.threshold}, level={self.level})"

    # 图像缓存池
    cache_pool = {}

    def __init__(self, template_path: str, region: Rect = None, threshold=0.95, level=None) -> None:
        super().__init__()
        self.template_path = template_path
        self.region = region
        self.threshold = threshold
        self.level = level
        self.template = None

    def match(self, image: cv2.Mat) -> RectMatchResult | NoneMatchResult:
        if self.template is None:
            if ImageTemplate.cache_pool.get(self.template_path):
                self.template = ImageTemplate.cache_pool[self.template_path]
            else:
                self.template = imread(self.template_path, cv2.IMREAD_UNCHANGED)
                ImageTemplate.cache_pool[self.template_path] = self.template

        result = match_template_best(image, self.template, self.region, self.threshold, self.level)

        if result is None:
            return NoneMatchResult()

        h, w = get_height(self.template), get_width(self.template)
        return RectMatchResult(result.x, result.y, w, h)

    @staticmethod
    def from_dict(data: dict):
        template_path = data.get('template_path')
        if template_path is None:
            raise ValueError("template_path must be specified")
        if not os.path.exists(template_path):
            raise FileNotFoundError(template_path)

        tmp_region: list[int] | tuple[int] | Rect | None = data.get('region', None)
        if isinstance(tmp_region, (list, tuple)):
            region = Rect(tmp_region[0], tmp_region[1], tmp_region[2], tmp_region[3])
        elif isinstance(tmp_region, Rect):
            region = tmp_region
        elif tmp_region is None:
            region = None
        else:
            raise TypeError("region must be list, tuple or Rect")

        threshold = data.get('threshold', 0.95)
        if threshold < 0 or threshold > 1:
            raise ValueError("threshold must be between 0 and 1")

        level: int | None = data.get('level', None)
        if level is not None and level < 0:
            raise ValueError("level must be greater than or equal to 0")

        return ImageTemplate(template_path, region, threshold, level)