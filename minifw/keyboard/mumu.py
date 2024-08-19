from minifw.common import MUMU_API_DLL_PATH, MuMuApi
from minifw.keyboard.keyboard import Keyboard


class MuMuKeyboard(Keyboard):
    def __init__(
            self,
            instance_index:int,
            emulator_install_path: str,
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
        self.dll_path = emulator_install_path + MUMU_API_DLL_PATH if dll_path is None else dll_path
        self.nemu = MuMuApi(self.dll_path)
        # 连接模拟器
        self.handle = self.nemu.connect(emulator_install_path, instance_index)

    def key_down(self, key: str) -> None:
        self.nemu.input_event_key_down(self.handle, self.display_id, key)

    def key_up(self, key: str) -> None:
        self.nemu.input_event_key_up(self.handle,self.display_id, key)