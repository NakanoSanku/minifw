import ctypes


class MuMuApi:
    def __init__(self, dll_path):
        self.nemu = ctypes.CDLL(dll_path)
        # 定义返回类型和参数类型
        self.nemu.nemu_connect.restype = ctypes.c_int
        self.nemu.nemu_connect.argtypes = [ctypes.c_wchar_p, ctypes.c_int]

        self.nemu.nemu_disconnect.argtypes = [ctypes.c_int]

        self.nemu.nemu_capture_display.restype = ctypes.c_int
        self.nemu.nemu_capture_display.argtypes = [
            ctypes.c_int,
            ctypes.c_uint,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_ubyte),
        ]

        self.nemu.nemu_input_text.restype = ctypes.c_int
        self.nemu.nemu_input_text.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_char_p,
        ]

        self.nemu.nemu_input_event_touch_down.restype = ctypes.c_int
        self.nemu.nemu_input_event_touch_down.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]

        self.nemu.nemu_input_event_touch_up.restype = ctypes.c_int
        self.nemu.nemu_input_event_touch_up.argtypes = [
            ctypes.c_int, ctypes.c_int]

        self.nemu.nemu_input_event_key_down.restype = ctypes.c_int
        self.nemu.nemu_input_event_key_down.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]

        self.nemu.nemu_input_event_key_up.restype = ctypes.c_int
        self.nemu.nemu_input_event_key_up.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]

    def connect(self, emulator_install_path, instance_index):
        return self.nemu.nemu_connect(emulator_install_path, instance_index)

    def disconnect(self, handle):
        return self.nemu.nemu_disconnect(handle)

    def capture_display(self, handle, display_id, buffer_size, width, height, pixels):
        return self.nemu.nemu_capture_display(
            handle, display_id, buffer_size, width, height, pixels
        )

    def input_text(self, handle, size, buf):
        return self.nemu.nemu_input_text(handle, size, buf)

    def input_event_touch_down(self, handle, display_id, xPoint, yPoint):
        return self.nemu.nemu_input_event_touch_down(handle, display_id, xPoint, yPoint)

    def input_event_touch_up(self, handle, display_id):
        return self.nemu.nemu_input_event_touch_up(handle, display_id)

    def input_event_key_down(self, handle, display_id, keyCode):
        return self.nemu.nemu_input_event_key_down(handle, display_id, keyCode)

    def input_event_key_up(self, handle, display_id, keyCode):
        return self.nemu.nemu_input_event_key_up(handle, display_id, keyCode)
