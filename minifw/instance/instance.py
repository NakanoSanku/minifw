import functools
import time
from dataclasses import dataclass
from threading import Thread
from time import sleep
from uuid import uuid4

import cv2
from loguru import logger

from minifw.cv import bytes2mat, rectangle, point, destroy_window
from minifw.keyboard import Keyboard
from minifw.matcher import MatchResult, Template
from minifw.matcher.result import RectMatchResult, PointMatchResult
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


@dataclass
class ScriptInstanceConfig:
    screencap_method: ScreenCap = None
    touch_method: Touch = None
    keyboard_method: Keyboard = None
    debug: bool = False
    draw_color: int | str = "#DC143C"
    draw_size: int = 1
    winname: str = str(uuid4())


class ScriptInstance(ScreenCap, Touch, Keyboard):
    def __init__(self, config: ScriptInstanceConfig):
        self.config = config
        self.imshow_flag = True
        self.imshow_thread = None

    def screencap_raw(self) -> bytes:
        if self.config.screencap_method is None:
            raise Exception("未指定截图方式")
        return self.config.screencap_method.screencap_raw()

    @performance_test
    def screencap(self) -> cv2.Mat:
        return bytes2mat(self.screencap_raw())

    @performance_test
    def click(self, x: int, y: int, duration: int = 100):
        if self.config.touch_method is None:
            raise Exception("未指定触摸方式")
        self.debug_log(f"Click at point({x},{y}) in {duration}ms")
        return self.config.touch_method.click(x, y, duration)

    @performance_test
    def swipe(self, points: list, duration: int = 300):
        if self.config.touch_method is None:
            raise Exception("未指定触摸方式")
        self.debug_log(f"Swipe from {points[0]} to {points[-1]} in {duration}ms")
        return self.config.touch_method.swipe(points, duration)

    @performance_test
    def find(self, template: Template) -> MatchResult:
        screen = self.screencap()
        result = template.match(screen)
        result.set_controller(self)
        if self.config.debug:
            logger.debug(f"Find {template} in {result.get()}")
            self.imshow_flag = False
            if self.imshow_thread is not None:
                self.imshow_thread.join()
            self.imshow_flag = True
            self.imshow_thread = Thread(target=self.draw_result_in_screen, args=(screen, result))
            self.imshow_thread.start()

        return result

    @performance_test
    def key_down(self, key: str) -> None:
        if self.config.keyboard_method is None:
            raise Exception("未指定键盘输入方式")
        self.debug_log(f"Key down {key}")
        self.config.keyboard_method.key_down(key)

    @performance_test
    def key_up(self, key: str) -> None:
        if self.config.keyboard_method is None:
            raise Exception("未指定键盘输入方式")
        self.debug_log(f"Key up {key}")
        self.config.keyboard_method.key_up(key)

    @performance_test
    def find_and_click(self, template: Template, duration: int = 100, algorithm=None) -> MatchResult:
        result = self.find(template)
        result.click(self, duration, algorithm) if algorithm else result.click(self, duration)
        return result

    def draw_result_in_screen(self, screen, result: MatchResult):
        # 如果result是RectMatchResult就进行方框绘制
        if isinstance(result, RectMatchResult):
            # 显示绘制方框的截图
            screen = rectangle(screen, result.get(), self.config.draw_color, self.config.draw_size)
        # 如果result是PointMatchResult就进行方框绘制
        elif isinstance(result, PointMatchResult):
            # 显示绘制点的截图
            screen = point(screen, result.get(), self.config.draw_size, self.config.draw_color)
        cv2.imshow(self.config.winname, screen)
        while self.imshow_flag:
            # 检查窗口是否关闭
            if cv2.getWindowProperty(self.config.winname, cv2.WND_PROP_VISIBLE) < 1:
                break
            # 检查是否有按键被按下
            if cv2.waitKey(1) != -1:
                break
        destroy_window(self.config.winname)

    def debug_log(self, msg: str):
        if self.config.debug:
            logger.debug(msg)


if __name__ == '__main__':
    from minifw.screencap import ADBCap
    from minifw.touch import ADBTouch
    from minifw.matcher.image import ImageTemplate

    screencap_method = ADBCap(serial="127.0.0.1:16384")
    touch_method = ADBTouch(serial="127.0.0.1:16384")
    config = ScriptInstanceConfig(screencap_method=screencap_method, touch_method=touch_method, debug=True)
    instance = ScriptInstance(config)
    t = ImageTemplate(r"C:\Users\KateT\Desktop\QQ截图20240819103933.png")
    instance.find(t).click(instance, duration=150)
    sleep(3)
    instance.find(t)
    pass
