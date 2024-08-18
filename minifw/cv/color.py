import math


class Color:
    """
    颜色工具类
    """
    @staticmethod
    def int2str(color_int):
        """
        int2str 16进制转颜色值的字符串

        Args:
            color_int (int): 0xFF112233

        Returns:
            颜色值的字符串 (str): 格式为 "#AARRGGBB"。
        """
        # 将整数RGB颜色值转换为16进制字符串
        hex_color = hex(color_int)[2:].upper().zfill(8)
        # 将16进制字符串转换为"AARRGGBB"格式的字符串
        a, r, g, b = [hex_color[i: i + 2] for i in range(0, 8, 2)]
        return f"#{a}{r}{g}{b}"

    @staticmethod
    def is_similar(color1: int, color2: int, threshold=4, algorithm="diff"):
        """
        isSimilar 返回两个颜色是否相似
        Args:
            color1 (int): 16进制颜色值
            color2 (int): 16进制颜色值
            threshold (int, optional): 相似度. Defaults to 4.
            algorithm (str, optional): 比较算法. Defaults to 'diff'.
                algorithm包括:
                    "diff": 差值匹配。与给定颜色的R、G、B差的绝对值之和小于threshold时匹配。
                    "rgb": rgb欧拉距离相似度。与给定颜色color的rgb欧拉距离小于等于threshold时匹配。
                    "rgb+": 加权rgb欧拉距离匹配(LAB Delta E)。
                    "hs": hs欧拉距离匹配。hs为HSV空间的色调值。
        - Returns:
            (两个颜色是否相似) bool:
        """
        # 差值匹配算法
        if algorithm == "diff":
            r1 = (color1 >> 16) & 0xFF
            g1 = (color1 >> 8) & 0xFF
            b1 = color1 & 0xFF
            r2 = (color2 >> 16) & 0xFF
            g2 = (color2 >> 8) & 0xFF
            b2 = color2 & 0xFF
            diff = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
            return diff <= threshold
        # RGB欧拉距离相似度算法
        elif algorithm == "rgb":
            r1 = (color1 >> 16) & 0xFF
            g1 = (color1 >> 8) & 0xFF
            b1 = color1 & 0xFF
            r2 = (color2 >> 16) & 0xFF
            g2 = (color2 >> 8) & 0xFF
            b2 = color2 & 0xFF
            diff = math.sqrt(pow(r1 - r2, 2) +
                             pow(g1 - g2, 2) + pow(b1 - b2, 2))
            return diff <= threshold
        # 加权RGB欧拉距离相似度算法
        elif algorithm == "rgb+":
            lab1 = rgb2lab(color1)
            lab2 = rgb2lab(color2)
            diff = deltaE(lab1, lab2)
            return diff <= threshold
        # HS欧拉距离相似度算法
        elif algorithm == "hs":
            hs1 = rgb2hs(color1)
            hs2 = rgb2hs(color2)
            diff = math.sqrt(pow(hs1[0] - hs2[0], 2) + pow(hs1[1] - hs2[1], 2))
            return diff <= threshold
        else:
            return False

    @staticmethod
    def str2int(color_str):
        """
        str2int 解析颜色值为16进制

        Args:
            color_str (str): "#112233"

        Returns:
            16进制颜色值 (int):
        """
        return int(color_str[1:], 16)

    @staticmethod
    def bgr2str(color_bgr):
        """
        bgr2str 将BGR颜色值转换为颜色字符串

        Args:
            color_bgr (list): [b,g,r]

        Returns:
            颜色字符串 (str): 格式为 "#RRGGBB"。
        """
        b, g, r = color_bgr
        return '#%02x%02x%02x' % (r, g, b)

    @staticmethod
    def str2bgr(color_str):
        """
        colorStrTobgr 将颜色字符串转换为BGR颜色值

        Args:
            color_str (str): "#RRGGBB"

        Returns:
            BGR颜色值 (list): [b,g,r]
        """
        color = Color.str2int(color_str)
        return [
            color & 0xFF,
            (color >> 8) & 0xFF,
            (color >> 16) & 0xFF,
        ]


# RGB转LAB


def rgb2lab(color):
    r = (color >> 16) & 0xFF
    g = (color >> 8) & 0xFF
    b = color & 0xFF
    r = r / 255
    g = g / 255
    b = b / 255
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
    return [l, a, b]


# LAB Delta E
def deltaE(lab1, lab2):
    l1 = lab1[0]
    a1 = lab1[1]
    b1 = lab1[2]
    l2 = lab2[0]
    a2 = lab2[1]
    b2 = lab2[2]
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


# RGB转HS
def rgb2hs(color):
    r = (color >> 16) & 0xFF
    g = (color >> 8) & 0xFF
    b = color & 0xFF
    r = r / 255
    g = g / 255
    b = b / 255
    maxVal = max(r, g, b)
    minVal = min(r, g, b)
    diff = maxVal - minVal
    if diff == 0:
        h = 0
    elif maxVal == r:
        h = (g - b) / diff
        if h < 0:
            h += 6
    elif maxVal == g:
        h = (b - r) / diff + 2
    else:
        h = (r - g) / diff + 4
    h = h / 6
    s = 0 if maxVal == 0 else diff / maxVal
    return [h, s]


if __name__ == "__main__":
    print(Color.str2bgr("#112233"))
    print(Color.bgr2str([51, 34, 17]))