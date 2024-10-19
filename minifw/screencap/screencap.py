from abc import ABC, abstractmethod
import cv2

class ScreenCap(ABC):

    @abstractmethod
    def screencap_raw(self) -> bytes:
        """截图未进行编码的源数据"""

    @abstractmethod
    def screencap(self) -> cv2.Mat:
        """截图opencv格式(未进行编码的图像)"""

    def save_screencap(self, filename="screencap.png"):
        """
        save_screencap 保存截图

        Args:
            filename (str, optional): 截图保存路径. Defaults to "screencap.png".
        """
        cv2.imwrite(filename,self.screencap())


