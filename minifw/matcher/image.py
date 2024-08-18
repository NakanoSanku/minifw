import cv2

from .result import MatchResult, NoneMatchResult
from .template import Template
from ..algo.generate import RegionPointGenerator, NormalDistributionPointGenerator
from ..common import Rect
from ..cv import match_template_best, imread, get_height, get_width
from ..touch import Touch


class ImageMatchResult(MatchResult):
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get(self):
        return self.x, self.y, self.w, self.h

    def click(self, controller: Touch, duration: int = 100,
              algorithm: RegionPointGenerator = NormalDistributionPointGenerator) -> bool:
        point = algorithm.generate(self.x, self.y, self.w, self.h)
        controller.click(point.x, point.y, duration)
        return True


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

    def match(self, image: cv2.Mat) -> ImageMatchResult | NoneMatchResult:
        if self.template is None:
            if ImageTemplate.cache_pool.get(self.template_path):
                self.template = ImageTemplate.cache_pool[self.template_path]
            else:
                self.template = imread(self.template_path, cv2.IMREAD_UNCHANGED)
                ImageTemplate.cache_pool[self.template_path] = self.template

        result = match_template_best(image, self.template,self.region, self.threshold, self.level)

        if result is None:
            return NoneMatchResult()

        h, w = get_height(self.template), get_width(self.template)
        return ImageMatchResult(result.x,result.y, w, h)
