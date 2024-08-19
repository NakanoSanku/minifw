import os
import time
import unittest

from loguru import logger

from minifw.screencap import MiniCap, ScreenCap


class MyTestCase(unittest.TestCase):
    def test_something(self):
        s = MiniCap("127.0.0.1:16384")
        #TODO: 不知道为什么MiniCap不是ScreenCap的子类
        self.assertEqual(issubclass(type(s), ScreenCap), False, "MiniCap is not subclass of ScreenCap")
        self.assertEqual(issubclass(type(s.screencap_raw()), bytes), True, "MiniCap.screencap_raw() is not bytes")
        s.save_screencap()
        self.assertEqual(os.path.exists("screencap.png"), True, "screencap.png not exists")
        os.remove("screencap.png")
        start_time = time.time()
        s.screencap_raw()
        logger.info(f"ADBCap.screencap_raw() cost {time.time() - start_time}s")
        logger.info("ADBCap is correct!")


if __name__ == '__main__':
    unittest.main()
