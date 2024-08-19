import cv2

from minifw.cv import bytes2mat
from minifw.keyboard import Keyboard
from minifw.matcher import MatchResult, Template
from minifw.screencap import ScreenCap
from minifw.touch import Touch


class ScriptInstance(ScreenCap, Touch, Keyboard):
    def __init__(self, screencap_method: ScreenCap = None, touch_method: Touch = None, keyboard_method: Keyboard = None,
                 debug=False):
        self.screencap_method = screencap_method
        self.touch_method = touch_method
        self.keyboard_method = keyboard_method
        self.debug = debug  #TODO: 添加调试模式
        self.cache_screen: cv2.Mat | None = None  #TODO: 添加画面检测
        self.timeout = 0  #TODO: 添加超时检测

    def screencap_raw(self) -> bytes:
        if self.screencap_method is None:
            raise Exception("未指定截图方式")
        return self.screencap_method.screencap_raw()

    def screencap(self) -> cv2.Mat:
        return bytes2mat(self.screencap_raw())

    def click(self, x: int, y: int, duration: int = 100):
        if self.touch_method is None:
            raise Exception("未指定触摸方式")
        return self.touch_method.click(x, y, duration)

    def swipe(self, points: list, duration: int = 300):
        if self.touch_method is None:
            raise Exception("未指定触摸方式")
        return self.touch_method.swipe(points, duration)

    def find(self, template: Template) -> MatchResult:
        return template.match(self.screencap())

    def key_down(self, key: str) -> None:
        if self.keyboard_method is None:
            raise Exception("未指定键盘输入方式")
        self.keyboard_method.key_down(key)

    def key_up(self, key: str) -> None:
        if self.keyboard_method is None:
            raise Exception("未指定键盘输入方式")
        self.keyboard_method.key_up(key)


if __name__ == '__main__':
    # screencap_method = ADBCap(serial="127.0.0.1:16384")
    # touch_method = MiniTouch(serial="127.0.0.1:16384")
    # instance = ScriptInstance(screencap_method, touch_method)
    # t = ImageTemplate(r"C:\Users\KateT\Desktop\QQ截图20240819103933.png",
    #                   region=Rect(800,110,200,600))
    # instance.find(t).click(instance,duration=1000)
    pass
