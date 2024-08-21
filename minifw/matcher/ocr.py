import cv2

from minifw.common import Rect
from minifw.cv import clip
from minifw.matcher import Template
from minifw.matcher.result import RectMatchResult, NoneMatchResult
from minifw.ocr import OcrService


class OCRTemplate(Template):
    def __str__(self) -> str:
        return f"OCRTemplate(text={self.text}, region={self.region}, threshold={self.threshold})"

    def __init__(self, text: str, region: Rect = None, threshold: float = 0.6, provider_name: str = None) -> None:
        self.text = text
        self.region = region
        self.threshold = threshold
        self.cache_result = None
        self.service = OcrService.get_provider(provider_name)

    def match(self, image: cv2.Mat) -> RectMatchResult | NoneMatchResult:
        x, y, w, h = self.region.x, self.region.y, self.region.w, self.region.h if self.region else (
            0, 0, image.shape[1], image.shape[0])
        image = clip(image, x, y, w, h) if self.region else image
        #TODO: 减少识别次数, 识别结果缓存
        result = self.service.run(image)
        if result is not None:
            for r in result:
                if r.text == self.text and r.confidence > self.threshold:
                    return RectMatchResult(r.region.x + x, r.region.y + y, r.region.w, r.region.h)
        return NoneMatchResult()
