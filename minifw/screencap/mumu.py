import ctypes

import numpy as np
from turbojpeg import TurboJPEG, TJSAMP_422

from minifw.common import MuMuApi, MUMU_API_DLL_PATH, TURBO_JPEG_DLL_PATH
from minifw.common.config import MUMU_INSTALL_PATH
from minifw.screencap.screencap import ScreenCap


class MuMuScreenCap(ScreenCap):
    def __init__(
            self,
            instance_index,
            emulator_install_path: str = MUMU_INSTALL_PATH,
            dll_path: str = None,
            display_id: int = 0,
            quality: int = 100,
            jpeg_subsample=TJSAMP_422
    ):
        """
        __init__ MumuApi 截图

        基于/shell/sdk/external_renderer_ipc.dll实现截图mumu模拟器

        Args:
            instance_index (int): 模拟器实例的编号
            emulator_install_path (str): 模拟器安装路径
            dll_path (str, optional): dll文件存放路径，一般会根据模拟器路径获取. Defaults to None.
            display_id (int, optional): 显示窗口id，一般无需填写. Defaults to 0.
        """
        self.quality = quality
        self.height = None
        self.width = None
        self.display_id = display_id
        self.instance_index = instance_index
        self.emulator_install_path = emulator_install_path
        self.dllPath = emulator_install_path + \
                       MUMU_API_DLL_PATH if dll_path is None else dll_path
        self.nemu = MuMuApi(self.dllPath)
        # 连接模拟器
        self.handle = self.nemu.connect(
            self.emulator_install_path, self.instance_index)
        self.__get_display_info()
        self.turbo_jpeg_encoder = TurboJPEG(TURBO_JPEG_DLL_PATH)
        self.jpeg_subsample = jpeg_subsample

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
        # 根据宽度和高度计算缓冲区大小
        self.buffer_size = self.width.value * self.height.value * 4
        # 创建一个足够大的缓冲区来存储像素数据
        self.pixels = (ctypes.c_ubyte * self.buffer_size)()

    def screencap_raw(self) -> bytes:
        self.width = ctypes.c_int(self.width.value)
        self.height = ctypes.c_int(self.height.value)
        result = self.nemu.capture_display(
            self.handle,
            self.display_id,
            self.buffer_size,
            self.width,
            self.height,
            self.pixels,
        )
        if result > 1:
            raise BufferError("截图错误")
        return self.__buffer2bytes()

    def __buffer2bytes(self):
        # Directly use the pixel buffer and reshape only once
        pixel_array = np.frombuffer(self.pixels, dtype=np.uint8).reshape(
            (self.height.value, self.width.value, 4))
        flipped_rgb_pixel_array = pixel_array[::-1, :, [2, 1, 0]]
        # TurboJPEG方案
        data = self.turbo_jpeg_encoder.encode(np.ascontiguousarray(
            flipped_rgb_pixel_array), quality=self.quality, jpeg_subsample=self.jpeg_subsample)
        # Opencv方案
        # _ ,data = cv2.imencode(self.encode,flipped_rgb_pixel_array)
        # Pillow方案
        # image = Image.fromarray(flipped_rgb_pixel_array)
        # encoded_image = io.BytesIO()
        # image.save(encoded_image, format='JPEG', quality=95)
        # encoded_image.seek(0)
        # data = encoded_image.getvalue()
        # _, data = cv2.imencode(self.encode, flipped_rgb_pixel_array)
        return data

    def __del__(self):
        self.nemu.disconnect(self.handle)


if __name__ == '__main__':
    cap = MuMuScreenCap(0,r"C:\Program Files\Netease\MuMu Player 12")
    cap.save_screencap()