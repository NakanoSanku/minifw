from abc import abstractmethod, ABC


class PusherOptions(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def to_dict(self):
        pass


class Pusher(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def send(self, options: PusherOptions) -> bool:
        pass
