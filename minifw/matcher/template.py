import json
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

    @staticmethod
    def from_dict(data: dict):
        pass

    @classmethod
    def from_json(cls, data: str):
        return cls.from_dict(json.loads(data))
