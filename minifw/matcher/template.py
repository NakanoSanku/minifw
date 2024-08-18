from abc import ABC, abstractmethod

import cv2

from .result import MatchResult


class Template(ABC):
    @abstractmethod
    def match(self, image:cv2.Mat) -> MatchResult:
        pass