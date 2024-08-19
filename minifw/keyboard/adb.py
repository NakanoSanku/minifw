from adbutils import adb

from minifw.keyboard.keyboard import Keyboard


class ADBKeyboard(Keyboard):
    def __init__(self, serial) -> None:
        self.adb = adb.device(serial)

    def key_down(self, key: str) -> None:
        self.adb.keyevent(key)

    def key_up(self, key: str) -> None:
        pass
