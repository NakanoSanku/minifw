from abc import ABC
from dataclasses import dataclass

from minifw.common import Rect


@dataclass
class OcrResult:
    text: str
    confidence: float
    region: Rect


class OcrProvider(ABC):
    """
    ocr 服务提供者，提供ocr服务
    """
    NAME = "OCR"

    def __init__(self):
        pass

    def run(self, image) -> list[OcrResult] | None:
        pass


class OcrService:
    """
    ocr 服务统一接口，使用ocr时先初始化OcrService
    """
    # ocr服务提供者们，调用OCR会从该提供池中,选择一个服务提供者调用
    provider_pool: list[OcrProvider] = []

    @staticmethod
    def add_provider(provider: OcrProvider):
        OcrService.provider_pool.append(provider)

    @staticmethod
    def get_provider(name: str = None):
        if len(OcrService.provider_pool) == 0:
            raise Exception("没有添加OCR服务提供者")
        if name is None:
            return OcrService.provider_pool[0]
        for provider in OcrService.provider_pool:
            #TODO: 同个服务商的多个实例实现负载均很
            if provider.NAME == name:
                return provider
        raise Exception("没有找到对应的OCR服务提供者")



