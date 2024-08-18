import cv2

from minifw.common import Rect
from minifw.cv import match_template_best, imread, get_height, get_width
from minifw.matcher.result import NoneMatchResult, RectMatchResult
from minifw.matcher.template import Template


class ImageTemplate(Template):
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
