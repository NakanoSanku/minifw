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

    def from_dict(self, data: dict):
        text = data.get("text")
        if text is None:
            raise ValueError("text must be not None")
        if not isinstance(text, str):
            raise TypeError("text must be str")

        tmp_region: list[int] | tuple[int] | Rect | None = data.get('region', None)
        if isinstance(tmp_region, (list, tuple)):
            region = Rect(tmp_region[0], tmp_region[1], tmp_region[2], tmp_region[3])
        elif isinstance(tmp_region, Rect):
            region = tmp_region
        elif tmp_region is None:
            region = None
        else:
            raise TypeError("region must be list, tuple or Rect")

        threshold = data.get('threshold', 0.6)
        if threshold < 0 or threshold > 1:
            raise ValueError("threshold must be between 0 and 1")

        provider_name = data.get("provider_name", None)
        return OCRTemplate(text, region, threshold, provider_name)
