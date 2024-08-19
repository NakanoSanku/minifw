import os

from .common import is_point_in_rect, is_rect_in_rect
from .dataclass import Point, RGB, Rect, LAB, HSV, ImageSize
from .mumuapi import MuMuApi

WORK_DIR = os.path.dirname(__file__)
TURBO_JPEG_DLL_PATH = f"{WORK_DIR}/bin/turbojpeg.dll"
MUMU_API_DLL_PATH = "/shell/sdk/external_renderer_ipc.dll"
