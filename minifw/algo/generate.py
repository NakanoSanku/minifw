from abc import ABC

import numpy as np

from minifw.common import Point


class Generator(ABC):
    @staticmethod
    def generate(*args, **kwargs):
        pass


class PointGenerator(Generator):
    @staticmethod
    def generate(*args, **kwargs) -> Point:
        pass


class RegionPointGenerator(PointGenerator):
    @staticmethod
    def generate(x, y, w, h) -> Point:
        pass


class NormalDistributionPointGenerator(RegionPointGenerator):
    @staticmethod
    def generate(x, y, w, h) -> Point:
        center_point = CenterPointGenerator.generate(x, y, w, h)
        while True:
            x1 = round(np.random.normal(center_point.x, w / 6))
            y1 = round(np.random.normal(center_point.y, h / 6))
            if x <= x1 <= x + w and y <= y1 <= y + h:
                break
        return Point(x1, y1)


class CenterPointGenerator(RegionPointGenerator):
    @staticmethod
    def generate(x, y, w, h) -> Point:
        return Point(x + w // 2, y + h // 2)


class OffsetPointGenerator(PointGenerator):
    @staticmethod
    def generate(x, y) -> Point:
        pass


class NoneOffsetPointGenerator(OffsetPointGenerator):
    @staticmethod
    def generate(x, y) -> Point:
        return Point(x, y)
