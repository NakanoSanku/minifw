from abc import ABC, abstractmethod

import cv2

from minifw.matcher.result import MatchResult


class Template(ABC):
    @abstractmethod
    def match(self, image: cv2.Mat) -> MatchResult:
        pass

    @abstractmethod
    def __str__(self) -> str:
        return "Template Desc"
