import ctypes
import time

from minifw.common import MuMuApi, MUMU_API_DLL_PATH
from minifw.common.config import MUMU_INSTALL_PATH
from minifw.touch.touch import Touch


class MuMuTouch(Touch):
    def __init__(
            self,
            instance_index,
            emulator_install_path: str = MUMU_INSTALL_PATH,
            dll_path: str = None,
            display_id: int = 0,
    ):
        """
        __init__ MumuApi 操作

        基于/shell/sdk/external_renderer_ipc.dll实现操作mumu模拟器

        Args:
            instance_index (int): 模拟器实例的编号
            emulator_install_path (str): 模拟器安装路径
            dll_path (str, optional): dll文件存放路径，一般会根据模拟器路径获取. Defaults to None.
            display_id (int, optional): 显示窗口id，一般无需填写. Defaults to 0.
        """
        self.display_id = display_id
        self.instance_index = instance_index
        self.emulator_install_path = emulator_install_path
        self.dll_path = emulator_install_path + \
                        MUMU_API_DLL_PATH if dll_path is None else dll_path
        self.nemu = MuMuApi(self.dll_path)
        # 连接模拟器
        self.handle = self.nemu.connect(
            self.emulator_install_path, self.instance_index)
        self.__get_display_info()

    def __get_display_info(self):
        self.width = ctypes.c_int(0)
        self.height = ctypes.c_int(0)
        result = self.nemu.capture_display(
            self.handle,
            self.display_id,
            0,
            ctypes.byref(self.width),
            ctypes.byref(self.height),
            None,
        )
        if result != 0:
            print("Failed to get the display size.")
            return None

    def click(self, x: int, y: int, duration: int = 100):
        x, y = self.xy_change(x, y)
        self.nemu.input_event_touch_down(self.handle, self.display_id, x, y)
        time.sleep(duration / 1000)
        self.nemu.input_event_touch_up(self.handle, self.display_id)

    def swipe(self, points: list, duration: int = 300):
        for point in points:
            x, y = self.xy_change(point[0], point[1])
            self.nemu.input_event_touch_down(self.handle, self.display_id, x, y)
            time.sleep(duration / len(points) / 1000)
        self.nemu.input_event_touch_up(self.handle, self.display_id)

    def xy_change(self, x, y):
        x, y = int(x), int(y)
        x, y = self.height.value - y, x
        return x, y

    def __del__(self):
        self.nemu.disconnect(self.handle)


if __name__ == '__main__':
    touch = MuMuTouch(0, r'C:\Program Files\Netease\MuMu Player 12')
    touch.click(100, 100)
    touch.swipe([(100, 100), (200, 200), (300, 300)])
