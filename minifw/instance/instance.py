import functools
import time

import cv2
from loguru import logger

from minifw.cv import bytes2mat
from minifw.keyboard import Keyboard
from minifw.matcher import MatchResult, Template
from minifw.screencap import ScreenCap
from minifw.touch import Touch


def performance_test(func):
    """装饰器：测量函数执行时间"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.config.debug:
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.debug(f"Function {func.__name__} executed in {elapsed_time * 1000:.6f}ms")
            return result
        else:
            return func(self, *args, **kwargs)

    return wrapper


class ScriptInstance(ScreenCap, Touch, Keyboard):
    def __init__(self, screencap_method: ScreenCap = None,touch_method: Touch = None, keyboard_method: Keyboard = None,debug: bool = False):
        self.debug = debug
        self.keyboard_method = keyboard_method
        self.touch_method = touch_method
        self.screencap_method = screencap_method

    def screencap_raw(self) -> bytes:
        if self.screencap_method is None:
            raise Exception("未指定截图方式")
        return self.screencap_method.screencap_raw()

    @performance_test
    def screencap(self) -> cv2.Mat:
        return bytes2mat(self.screencap_raw())

    @performance_test
    def click(self, x: int, y: int, duration: int = 150):
        if self.touch_method is None:
            raise Exception("未指定触摸方式")
        self.debug_log(f"Click at point({x},{y}) in {duration}ms")
        return self.touch_method.click(x, y, duration)

    @performance_test
    def swipe(self, points: list, duration: int = 500):
        if self.touch_method is None:
            raise Exception("未指定触摸方式")
        self.debug_log(f"Swipe from {points[0]} to {points[-1]} in {duration}ms")
        return self.touch_method.swipe(points, duration)

    @performance_test
    def find(self, template: Template) -> MatchResult:
        screen = self.screencap()
        result = template.match(screen)
        result.set_controller(self)
        if self.debug:
            logger.debug(f"Find {template} in {result.get()}")
        return result

    @performance_test
    def key_down(self, key: str) -> None:
        if self.keyboard_method is None:
            raise Exception("未指定键盘输入方式")
        self.debug_log(f"Key down {key}")
        self.keyboard_method.key_down(key)

    @performance_test
    def key_up(self, key: str) -> None:
        if self.keyboard_method is None:
            raise Exception("未指定键盘输入方式")
        self.debug_log(f"Key up {key}")
        self.keyboard_method.key_up(key)

    @performance_test
    def find_and_click(self, template: Template, duration: int = 150, algorithm=None) -> MatchResult:
        result = self.find(template)
        result.click(self, duration, algorithm) if algorithm else result.click(self, duration)
        return result

    def debug_log(self, msg: str):
        if self.debug:
            logger.debug(msg)

    @staticmethod
    def sleep(duration: int):
        time.sleep(duration/1000)


if __name__ == '__main__':
    from minifw.screencap import ADBCap
    from minifw.touch import ADBTouch
    from minifw.matcher import  ImageTemplate


    screencap_method = ADBCap(serial="127.0.0.1:16384")
    touch_method = ADBTouch(serial="127.0.0.1:16384")
    instance = ScriptInstance(screencap_method=screencap_method, touch_method=touch_method, debug=True)
    t = ImageTemplate(r"C:\Users\KateT\Desktop\QQ截图20240819103933.png")
    instance.find(t).click(instance, duration=150)
    instance.sleep(3)
    instance.find(t)
    pass
