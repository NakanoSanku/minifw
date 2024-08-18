import math
import re

from minifw.common import RGB, LAB, HSV


class Color:
    """
    颜色工具类
    """

    @staticmethod
    def rgb2str(color: RGB) -> str:
        return f"#{color.r:02x}{color.g:02x}{color.b:02x}"

    @staticmethod
    def rgb2int(color: RGB) -> int:
        return color.r << 16 | color.g << 8 | color.b

    @staticmethod
    def str2rgb(color: str) -> RGB:
        if color[0] == "#":
            color = color[1:]
        if Color.is_hex_color(color):
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            return RGB(r, g, b)
        else:
            raise ValueError("Invalid color format")

    @staticmethod
    def int2rgb(color: int) -> RGB:
        return RGB((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

    @staticmethod
    def rgb2lab(color: RGB) -> LAB:
        r, g, b = Color.normalize_rgb(color)
        if r > 0.04045:
            r = pow((r + 0.055) / 1.055, 2.4)
        else:
            r = r / 12.92
        if g > 0.04045:
            g = pow((g + 0.055) / 1.055, 2.4)
        else:
            g = g / 12.92
        if b > 0.04045:
            b = pow((b + 0.055) / 1.055, 2.4)
        else:
            b = b / 12.92
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        x = x / 0.95047
        y = y / 1.00000
        z = z / 1.08883
        if x > 0.008856:
            x = pow(x, 1 / 3)
        else:
            x = (7.787 * x) + (16 / 116)
        if y > 0.008856:
            y = pow(y, 1 / 3)
        else:
            y = (7.787 * y) + (16 / 116)
        if z > 0.008856:
            z = pow(z, 1 / 3)
        else:
            z = (7.787 * z) + (16 / 116)
        l = (116 * y) - 16
        a = 500 * (x - y)
        b = 200 * (y - z)
        return LAB(l, a, b)

    @staticmethod
    def normalize_rgb(color: RGB):
        r = (color.r >> 16) & 0xFF
        g = (color.g >> 8) & 0xFF
        b = color.b & 0xFF
        r = r / 255
        g = g / 255
        b = b / 255
        return [r, g, b]

    @staticmethod
    def rgb2hsv(color: RGB) -> HSV:
        r, g, b = Color.normalize_rgb(color)
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        if diff == 0:
            h = 0
        elif max_val == r:
            h = (g - b) / diff
            if h < 0:
                h += 6
        elif max_val == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        h = h / 6
        s = 0 if max_val == 0 else diff / max_val
        return HSV(h=h, s=s, v=0)

    @staticmethod
    def deltaE(lab1: LAB, lab2: LAB):
        l1, a1, b1 = lab1.l, lab1.a, lab1.b
        l2, a2, b2 = lab2.l, lab2.a, lab2.b
        c1 = math.sqrt(pow(a1, 2) + pow(b1, 2))
        c2 = math.sqrt(pow(a2, 2) + pow(b2, 2))
        dc = c1 - c2
        dl = l1 - l2
        da = a1 - a2
        db = b1 - b2
        dh = math.sqrt(pow(da, 2) + pow(db, 2) - pow(dc, 2))
        k1 = 0.045
        k2 = 0.015
        sl = 1
        kc = 1
        kh = 1
        if l1 < 16:
            sl = (k1 * pow(l1 - 16, 2)) / 100
        if c1 < 16:
            kc = k1 * pow(c1, 2) / 100 + 1
        if dh < 180:
            kh = k2 * (dh ** 2) / 100 + 1
        return math.sqrt(
            pow(dl / (sl * k1), 2) + pow(dc / (kc * kc), 2) + pow(dh / (kh * kh), 2)
        )

    @staticmethod
    def is_similar(color1: RGB, color2: RGB, threshold=4, diff_algo="diff"):
        """
        isSimilar 返回两个颜色是否相似
        Args:
            color1 (int): 16进制颜色值
            color2 (int): 16进制颜色值
            threshold (int, optional): 相似度. Defaults to 4.
            diff_algo (str, optional): 比较算法. Defaults to 'diff'.
                "diff": 差值匹配。与给定颜色的R、G、B差的绝对值之和小于threshold时匹配。
                "rgb": rgb欧拉距离相似度。与给定颜色color的rgb欧拉距离小于等于threshold时匹配。
                "rgb+": 加权rgb欧拉距离匹配(LAB Delta E)。
                "hs": hs欧拉距离匹配。hs为HSV空间的色调值。
        - Returns:
            (两个颜色是否相似) bool:
        """
        # 差值匹配算法
        if diff_algo == "diff":
            diff = (abs(color1.r - color2.r) +
                    abs(color1.g - color2.g) +
                    abs(color1.b - color2.b))
            return diff <= threshold
        # RGB欧拉距离相似度算法
        elif diff_algo == "rgb":
            diff = math.sqrt(pow(color1.r - color2.r, 2) +
                             pow(color1.g - color2.g, 2) +
                             pow(color1.b - color2.b, 2))
            return diff <= threshold
        # 加权RGB欧拉距离相似度算法
        elif diff_algo == "rgb+":
            lab1 = Color.rgb2lab(color1)
            lab2 = Color.rgb2lab(color2)
            diff = Color.deltaE(lab1, lab2)
            return diff <= threshold
        # HS欧拉距离相似度算法
        elif diff_algo == "hs":
            hs1 = Color.rgb2hsv(color1)
            hs2 = Color.rgb2hsv(color2)
            diff = math.sqrt(pow(hs1.h - hs2.h, 2) + pow(hs1.s - hs2.s, 2))
            return diff <= threshold
        else:
            return False

    @staticmethod
    def to_rgb(color: int | str | RGB) -> RGB:
        if isinstance(color, int):
            return Color.int2rgb(color)
        elif isinstance(color, str):
            return Color.str2rgb(color)
        elif isinstance(color, RGB):
            return color
        else:
            raise ValueError("Invalid color format")

    @staticmethod
    def is_hex_color(color: str):
        # 正则表达式匹配带或不带#号的16进制颜色值
        pattern = r'^#?[A-Fa-f0-9]{6}$'
        return bool(re.match(pattern, color))


if __name__ == "__main__":
    print(Color.str2rgb("#112233"))
    print(Color.int2rgb(0x112233))
    print(0x112233)
    print(Color.rgb2int(RGB(17, 34, 51)))
    print(Color.rgb2str(RGB(17, 34, 51)))

    print(Color.is_similar(RGB(18, 37, 52), RGB(17, 34, 51)))
