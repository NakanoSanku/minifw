import subprocess

import cv2
import requests
import numpy as np
from adbutils import adb
from loguru import logger

from minifw.common.exception import ADBDeviceUnFound
from minifw.screencap.config import DROIDCAST_APK_ANDROID_PATH, DROIDCAST_APK_PATH, DROIDCAST_APK_VERSION, ADB_EXECUTOR, \
    DROIDCAST_PORT, \
    DROIDCAST_APK_PACKAGE_NAME, DROIDCAST_PM_PATH_SHELL, DROIDCAST_START_CMD
from minifw.screencap.screencap import ScreenCap


class DroidCast(ScreenCap):
    def __init__(self, serial, display_id: int = None) -> None:
        """
        __init__ DroidCast截图方法

        Args:
            serial (str): 设备id
            display_id (int): 显示器id use `adb shell dumpsys SurfaceFlinger --display-id` to get
        """
        if serial not in [device.serial for device in adb.device_list()]:
            raise ADBDeviceUnFound("设备不存在，请检查是否链接设备成功")
        self.__adb = adb.device(serial)
        self.__class_path = DROIDCAST_APK_ANDROID_PATH
        self.__display_id = display_id
        self.__droidcast_session = requests.Session()
        self.__droidcast_format = 'raw'
        self.__install()
        self.__start()
        self.width = self.__adb.window_size().width
        self.height = self.__adb.window_size().height

    def __install(self):
        if DROIDCAST_APK_PACKAGE_NAME not in self.__adb.list_packages():
            self.__adb.install(DROIDCAST_APK_PATH, nolaunch=True)
        else:
            if self.__adb.package_info(DROIDCAST_APK_PACKAGE_NAME)['version_name'] != DROIDCAST_APK_VERSION:
                self.__adb.uninstall(DROIDCAST_APK_PACKAGE_NAME)
                self.__adb.install(DROIDCAST_APK_PATH, nolaunch=True)

    def __start_droidcast(self):
        out = self.__adb.shell(DROIDCAST_PM_PATH_SHELL)
        self.__class_path = "CLASSPATH=" + out.split(":")[1]
        start_droidcast_cmd = DROIDCAST_START_CMD
        adb_command = [ADB_EXECUTOR, "-s", self.__adb.serial,
                       "shell", self.__class_path, start_droidcast_cmd]
        if self.__display_id:
            adb_command.extend(["--display_id={}".format(self.__display_id)])
        logger.info(adb_command)
        self.__droidcast_popen = subprocess.Popen(
            adb_command,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    def __forward_port(self):
        self.__droidcast_port = self.__adb.forward_port(DROIDCAST_PORT)
        self.__droidcast_url = f"http://localhost:{self.__droidcast_port}/screenshot?format={self.__droidcast_format}"

    def __start(self):
        self.__start_droidcast()
        self.__forward_port()
        self.screencap_raw()
        logger.info("DroidCast启动完成")

    def __stop(self):
        if self.__droidcast_popen.poll() is None:
            self.__droidcast_popen.kill()  # 关闭管道

    def screencap_raw(self) -> bytes:
        try:
            return self.__droidcast_session.get(self.__droidcast_url, timeout=3).content
        except requests.exceptions.ConnectionError:
            self.__stop()
            self.__start()
            return self.screencap_raw()

    def __del__(self):
        self.__stop()

    def __str__(self) -> str:
        return "DroidCast-url:{}".format(self.__droidcast_url)

    def screencap(self) -> cv2.Mat:
        raw = self.screencap_raw()
        arr = np.frombuffer(raw[:self.width * self.height * 4], np.uint8).reshape((self.height, self.width, 4))
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

if __name__ == '__main__':
    import cv2
    import numpy as np
    import time
    d = DroidCast(serial="127.0.0.1:16384")
    s= time.time()
    np_arr = d.screencap()
    print((time.time() - s) * 1000)
    cv2.imshow("",np_arr)
    cv2.waitKey(0)