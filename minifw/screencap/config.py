import os
import platform

from adbutils import adb_path

DEFAULT_HOST = "127.0.0.1"
WORK_DIR = os.path.dirname(__file__)

# system
# 'Linux', 'Windows' or 'Darwin'.
SYSTEM_NAME = platform.system()
NEED_SHELL = SYSTEM_NAME != "Windows"
ADB_EXECUTOR = adb_path()

# MINICAP
MINICAP_PATH = "{}/bin/minicap/libs".format(WORK_DIR)
MINICAPSO_PATH = "{}/bin/minicap/jni".format(WORK_DIR)
MNC_HOME = "/data/local/tmp/minicap"
MNC_SO_HOME = "/data/local/tmp/minicap.so"
MINICAP_COMMAND = ["LD_LIBRARY_PATH=/data/local/tmp",
                   "/data/local/tmp/minicap"]
MINICAP_START_TIMEOUT = 3


# DroidCast
DROIDCAST_PORT = 53516
DROIDCAST_APK_PACKAGE_NAME = "com.rayworks.droidcast"
DROIDCAST_PM_PATH_SHELL = "pm path {}".format(DROIDCAST_APK_PACKAGE_NAME)
DROIDCAST_START_CMD = "exec app_process / {}.Main".format(DROIDCAST_APK_PACKAGE_NAME)

DROIDCAST_APK_VERSION = "1.4.1"
DROIDCAST_APK_NAME_PREFIX = "DroidCast_"
DROIDCAST_APK_PATH = "{}/bin/{}{}.apk".format(
    WORK_DIR, DROIDCAST_APK_NAME_PREFIX, DROIDCAST_APK_VERSION)
DROIDCAST_APK_ANDROID_PATH = "/data/local/tmp/{}{}.apk".format(
    DROIDCAST_APK_NAME_PREFIX, DROIDCAST_APK_VERSION)
