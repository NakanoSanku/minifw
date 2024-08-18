import math
from typing import Sequence

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from minifw.common import Point, RGB, Rect, ImageSize, is_rect_in_rect
from minifw.cv.color import Color

RED = RGB(b=0, g=0, r=255)
DEFAULT_LINE_TYPE = cv2.LINE_AA  # 默认线的类型为抗锯齿
DEFAULT_COLOR = RED  # 默认颜色为红色
DEFAULT_SHIFT = 0
DEFAULT_THICKNESS = 1

DEFAULT_FONT_PATH = 'simsun.ttc'
DEFAULT_FONT_SIZE = 20


def imread(filename: str, flags: int = cv2.IMREAD_COLOR) -> cv2.Mat:
    data = np.fromfile(filename, dtype=np.uint8)
    return cv2.imdecode(data, flags)


def imwirte(filename: str, img: cv2.Mat, ext: str = ".png", params: Sequence[int] = None) -> None:
    if params:
        cv2.imencode(ext, img, params)[1].tofile(filename)
    else:
        cv2.imencode(ext, img)[1].tofile(filename)


def imshow(img: cv2.Mat, winname: str = "", wait=True) -> None:
    cv2.imshow(winname, img)
    if wait:
        cv2.waitKey(0)


def line(img: cv2.Mat, pt1: Point, pt2: Point, color: str | int | RGB = DEFAULT_COLOR,
         thickness: int = DEFAULT_THICKNESS, line_type: int = DEFAULT_LINE_TYPE, shift: int = DEFAULT_SHIFT):
    rgb = Color.to_rgb(color)
    bgr = (rgb.b, rgb.g, rgb.r)
    return cv2.line(img, (pt1.x, pt1.y), (pt2.x, pt2.y), bgr, thickness, line_type, shift)


def rectangle(img: cv2.Mat, region: Rect, color: str | int | RGB == DEFAULT_COLOR, thickness: int = DEFAULT_THICKNESS,
              line_type: int = DEFAULT_LINE_TYPE, shift: int = DEFAULT_SHIFT):
    rgb = Color.to_rgb(color)
    bgr = (rgb.b, rgb.g, rgb.r)
    return cv2.rectangle(img, (region.x, region.y), (region.x + region.w, region.y + region.h), bgr, thickness,
                         line_type, shift)


def put_text(img: cv2.Mat, text: str, position: Point, color: str | int | RGB = DEFAULT_COLOR,
             font_size: int = DEFAULT_FONT_SIZE,
             font_path: str = DEFAULT_FONT_PATH):
    rgb = Color.to_rgb(color)
    # 将OpenCV图像转换为Pillow图像
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # 创建Pillow的绘图对象
    draw = ImageDraw.Draw(img_pil)

    # 加载字体
    font = ImageFont.truetype(font_path, font_size)

    # 绘制文本
    draw.text((position.x, position.y), text, font=font, fill=(rgb.r, rgb.g, rgb.b))

    # 将Pillow图像转换回OpenCV格式
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    return img


def get_pixel(img: cv2.Mat, x: int, y: int) -> str:
    b, g, r = img[y, x]
    return Color.rgb2str(RGB(r, g, b))


def get_width(img: cv2.Mat):
    return img.shape[1]


def get_height(img: cv2.Mat):
    return img.shape[0]


def clip(img: cv2.Mat, x: int, y: int, w: int, h: int):
    if not is_rect_in_rect(Rect(x, y, w, h), Rect(0, 0, get_width(img), get_height(img))):
        raise ValueError("The rectangle is not in the image")
    return img[y:y + h, x:x + w]


def resize(src: cv2.Mat, dsize: ImageSize, interpolation=cv2.INTER_LINEAR) -> cv2.Mat:
    return cv2.resize(src, (dsize.width, dsize.height), interpolation=interpolation)


def scale(src: cv2.Mat, fx: float = 1, fy: float = 1, interpolation=cv2.INTER_LINEAR) -> cv2.Mat:
    return cv2.resize(src, None, fx=fx, fy=fy, interpolation=interpolation)


def cvt_color(src: cv2.Mat, code: int):
    return cv2.cvtColor(src, code)


def threshold(src: cv2.Mat, thresh: float, max_val: float = 255, threshold_type=cv2.THRESH_BINARY):
    return cv2.threshold(src, thresh, max_val, threshold_type)


def select_pyramid_level(img, template: cv2.Mat):
    min_dim = min(img.shape[0], img.shape[1],
                  template.shape[0], template.shape[1])
    if min_dim < 32:
        return 0
    max_level = int(math.log2(min_dim // 16))
    return min(6, max_level)


def generate_pyramid(img, level: int):
    pyramid = [img]
    for _ in range(level):
        img = cv2.pyrDown(img)
        pyramid.append(img)
    return pyramid


def find_matches(res: cv2.Mat, match_threshold: float = 0.95):
    loc = np.where(res >= match_threshold)
    return [pt for pt in zip(*loc[::-1])]


def transparent_to_mask(img, alphaThreshold=127):
    if img.shape[2] != 4:
        raise ValueError("Create Mask Must Be BGRA Or RGBA")
    alpha = img[:, :, 3]
    # 透明度阈值设置成127,透明度超过127的将设置成1,否则设置成0，255表示透明，0代表不透明
    _, mask = threshold(alpha, alphaThreshold, 1)
    return mask


def match_template(img: cv2.Mat, template: cv2.Mat, region: Rect = None, match_threshold: float = 0.95,
                   max_result: int = 5,
                   method: int = cv2.TM_CCOEFF_NORMED) -> list[Point]:
    # 设置查找区域
    x, y, w, h = (region.x, region.y, region.w, region.h) if region else (0, 0, img.shape[1], img.shape[0])
    img = clip(img, x, y, w, h)
    # 为带A通道的template创建掩膜
    mask = transparent_to_mask(template) if img.shape[2] != 4 else None
    # # 对图像和模板进行灰度化
    # img = grayscale(img)
    # template = grayscale(template)

    matches = []
    res = cv2.matchTemplate(
        img, template, method, mask=mask) if mask else cv2.matchTemplate(img, template, method)

    loc = find_matches(res, match_threshold)

    for pt in loc[:max_result]:
        match = Point(pt[0] + x, pt[1] + y)
        if not any(np.allclose((match.x, match.y), (m.x, m.y)) for m in matches):
            matches.append(match)

    return matches


def match_template_best(img: cv2.Mat, template: cv2.Mat, region: Rect = None, match_threshold: float = 0.95,
                        level: int = None,
                        method: int = cv2.TM_CCOEFF_NORMED) -> Point | None:
    # 设置查找区域
    x, y, w, h = (region.x, region.y, region.w, region.h) if region else (0, 0, img.shape[1], img.shape[0])
    img = clip(img, x, y, w, h)

    # 设置金字塔等级
    if level is None:
        level = select_pyramid_level(img, template)

    # 创建图像金字塔列表
    img_array = generate_pyramid(img, level)
    template_array = generate_pyramid(template, level)
    mask_array = []
    if img.shape[2] == 4:
        # 为带A通道的template创建掩膜
        mask_array = [transparent_to_mask(t) for t in template_array]
    for i in reversed(range(level + 1)):
        img_level = img_array[i]
        template_level = template_array[i]
        mask_level = mask_array[i] if img.shape[2] == 4 else None
        res = cv2.matchTemplate(img_level, template_level, method, mask=mask_level) if img.shape[
                                                                                           2] == 4 else cv2.matchTemplate(
            img_level, template_level, method)

        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > match_threshold:
            return Point(max_loc[0] * (2 ** i) + x, max_loc[1] * (2 ** i) + y)
    return None


def find_color_inner(img: cv2.Mat, color: int | str | RGB, region: Rect = None, color_threshold: int = 4):
    rgb = Color.to_rgb(color)
    bgr = [rgb.b, rgb.g, rgb.r]
    lowerBound = np.array(
        [max(color - color_threshold, 0) for color in bgr], dtype=np.uint8
    )
    upperBound = np.array(
        [min(color + color_threshold, 255) for color in bgr], dtype=np.uint8
    )
    x, y, w, h = (region.x, region.y, region.w, region.h) if region else [0, 0, img.shape[1], img.shape[0]]
    img = clip(img, x, y, w, h)
    mask = cv2.inRange(img, lowerBound, upperBound)
    return cv2.findNonZero(mask)


def find_color(img: cv2.Mat, color: int | str | RGB, region: Rect = None, color_threshold: int = 4) -> Point | None:
    x, y = (region.x, region.y) if region else [0, 0]
    result = find_color_inner(img, color, region, color_threshold)
    if result is None:
        return None
    point = [e for e in result[0][0]]
    return Point(point[0] + x, point[1] + y)


def find_all_points_color(img: cv2.Mat, color: int | str | RGB, region: Rect = None, color_threshold: int = 4) -> list[
                                                                                                                      Point] | None:
    x, y = (region.x, region.y) if region else [0, 0]
    result = find_color_inner(img, color, region, color_threshold)
    if result is None:
        return None
    points = [(p[0][0], p[0][1]) for p in result]
    return [Point(point[0] + x, point[1] + y) for point in points]


def find_multi_colors(img: cv2.Mat, firstColor: int | str | RGB, colors: list[tuple[int, int, int | str | RGB]],
                      region: Rect = None,
                      color_threshold: int = 4) -> Point | None:
    first_color_points = find_all_points_color(img, firstColor, region=region, color_threshold=color_threshold)
    if first_color_points is None:
        return None
    for result in first_color_points:
        for x, y, target_color in colors:
            offset_color = Color.to_rgb(get_pixel(img, x + result.x, y + result.y))
            pre_color = Color.to_rgb(target_color)
            is_similar = Color.is_similar(offset_color, pre_color, threshold=color_threshold)
            if not is_similar:
                result = None
                break
        if result is not None:
            return result
    return None


# TODO: 添加特征点匹配


if __name__ == "__main__":
    image = imread(r"C:\Users\KateT\Desktop\QQ截图20240817084747.png")
    text_image = put_text(image, "HELLO WORLD! 四十i是的是isi皇帝", Point(100, 100), font_size=50)
    imshow(text_image)
