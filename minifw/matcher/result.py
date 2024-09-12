from abc import ABC, abstractmethod

from minifw.algo import (RegionPointGenerator, NormalDistributionPointGenerator, OffsetPointGenerator,
                         NoneOffsetPointGenerator)
from minifw.common import Rect, Point
from minifw.touch import Touch


class MatchResult(ABC):
    def __init__(self) -> None:
        self.controller = None

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def click(self, controller, duration=100, algorithm=None) -> bool:
        pass

    def set_controller(self, controller: Touch):
        self.controller = controller

    @abstractmethod
    def __str__(self) -> str:
        return str(self.get())

    def is_emtpy(self):
        return self.get() is None


class NoneMatchResult(MatchResult):
    def __str__(self) -> str:
        return "Empty MatchResult"

    def __init__(self) -> None:
        super().__init__()

    def get(self):
        return None

    def click(self, *args, **kwargs) -> bool:
        return False


class RectMatchResult(MatchResult):
    def __str__(self) -> str:
        return f"Rect MatchResult:{self.get()}"

    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get(self) -> Rect:
        return Rect(self.x, self.y, self.w, self.h)

    def click(self, controller: Touch = None, duration: int = 150,
              algorithm: RegionPointGenerator = NormalDistributionPointGenerator) -> bool:
        point = algorithm.generate(self.x, self.y, self.w, self.h)
        controller = self.controller if controller is None else controller
        controller.click(point.x, point.y, duration)
        return True


class PointMatchResult(MatchResult):
    def __str__(self) -> str:
        return f"Point MatchResult:{self.get()}"

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def get(self) -> Point:
        return Point(self.x, self.y)

    def click(self, controller: Touch = None, duration: int = 150,
              algorithm: OffsetPointGenerator = NoneOffsetPointGenerator) -> bool:
        x, y = algorithm.generate(self.x, self.y)
        controller = self.controller if controller is None else controller
        controller.click(x, y, duration)
        return True
