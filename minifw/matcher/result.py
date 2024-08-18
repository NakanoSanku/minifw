from abc import ABC, abstractmethod


class MatchResult(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def click(self, touch, duration, algorithm):
        pass


class NoneMatchResult(MatchResult):
    def __init__(self) -> None:
        super().__init__()

    def get(self):
        return None

    def click(self, *args, **kwargs):
        pass
