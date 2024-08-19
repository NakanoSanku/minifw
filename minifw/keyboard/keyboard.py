from abc import ABC, abstractmethod


class Keyboard(ABC):
    @abstractmethod
    def key_down(self, key: str) -> None:
        """
        按下按键
        :param key: 按键
        :return:
        """
        pass

    @abstractmethod
    def key_up(self, key: str) -> None:
        """
        松开按键
        :param key:
        :return:
        """
        pass


