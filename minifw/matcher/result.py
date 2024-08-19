from abc import ABC, abstractmethod

from minifw.algo import (RegionPointGenerator, NormalDistributionPointGenerator, OffsetPointGenerator,
                         NoneOffsetPointGenerator)
from minifw.common import Rect
from minifw.touch import Touch


class MatchResult(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def click(self, touch, duration=100, algorithm=None) -> bool:
        pass


class NoneMatchResult(MatchResult):
    def __init__(self) -> None:
        super().__init__()

    def get(self):
        return None

    def click(self, *args, **kwargs) -> bool:
        return False


class RectMatchResult(MatchResult):
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get(self):
        return Rect(self.x, self.y, self.w, self.h)

    def click(self, controller: Touch, duration: int = 100,
              algorithm: RegionPointGenerator = NormalDistributionPointGenerator) -> bool:
        point = algorithm.generate(self.x, self.y, self.w, self.h)
        controller.click(point.x, point.y, duration)
        return True

class PointMatchResult(MatchResult):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y

    def click(self, touch: Touch, duration: int = 100, algorithm: OffsetPointGenerator = NoneOffsetPointGenerator) -> bool:
        x, y = algorithm.generate(self.x, self.y)
        touch.click(x, y, duration)
        return True