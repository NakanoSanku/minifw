import os.path
import time
import unittest

from loguru import logger

from minifw.screencap import ADBCap, ScreenCap


class ADBCapTestCase(unittest.TestCase):
    def test_something(self):
        s = ADBCap("127.0.0.1:16384")
        self.assertEqual(issubclass(type(s), ScreenCap), True, "ADBCap is not subclass of ScreenCap")
        self.assertEqual(issubclass(type(s.screencap_raw()), bytes),True, "ADBCap.screencap_raw() is not bytes")
        s.save_screencap()
        self.assertEqual(os.path.exists("screencap.png"), True, "screencap.png not exists")
        os.remove("screencap.png")
        start_time = time.time()
        s.screencap_raw()
        logger.info(f"ADBCap.screencap_raw() cost {time.time() - start_time}s")
        logger.info("ADBCap is correct!")

if __name__ == '__main__':
    unittest.main()
