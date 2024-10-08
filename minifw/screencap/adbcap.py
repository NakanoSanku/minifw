import subprocess

from adbutils import adb

from minifw.common.exception import ADBDeviceUnFound
from minifw.screencap.config import ADB_EXECUTOR
from minifw.screencap.screencap import ScreenCap


class ADBCap(ScreenCap):
    def __init__(self, serial, display_id=None) -> None:
        """
        __init__ ADB 截图方式

        Args:
            serial (str): 设备id
        """
        if serial not in [device.serial for device in adb.device_list()]:
            raise ADBDeviceUnFound("设备不存在，请检查是否链接设备成功")
        self.__adb = adb.device(serial)
        self.__display_id = display_id

    def screencap_raw(self) -> bytes:
        """
        截图并以字节流的形式返回Android设备的屏幕。

        :return: 截图的字节数据。
        """
        try:
            adb_command = [ADB_EXECUTOR, "-s", self.__adb.serial, "exec-out", "screencap", "-p"]
            if self.__display_id:
                adb_command.extend(["-d", str(self.__display_id)])
            process = subprocess.Popen(
                adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            data, err = process.communicate(timeout=10)

            if process.returncode == 0 and data:
                return data
            else:
                raise subprocess.TimeoutExpired(None, timeout=10, stderr=err)
        except subprocess.TimeoutExpired as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Error while screencapping the device: {e}")


