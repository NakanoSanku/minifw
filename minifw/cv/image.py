import math
from typing import Sequence
import cv2
import numpy as np

from minicv.color import Colors

RED = (0, 0, 255)
DEFAULT_LINE_TYPE = cv2.LINE_AA  # 默认线的类型为抗锯齿
DEFAULT_COLOR = RED  # 默认颜色为红色
DEFAULT_SHIFT = 0
DEFAULT_THICKNESS = 1


def imread(filename: str, flags: int = cv2.IMREAD_COLOR) -> cv2.Mat:
    """
    Read an image from a file.

    Parameters:
        filename (str): The path to the image file.
        flags (int): The flags used to read the image. Default is cv2.IMREAD_COLOR.

    Returns:
        cv2.Mat: The image data read from the file.

    Example:
        img = imread("支持中文.jpg")
    """
    # Use np.fromfile to read the file content and use cv2.imdecode to decode it into image data.
    data = np.fromfile(filename, dtype=np.uint8)
    image = cv2.imdecode(data, flags)
    return image


def imwirte(filename: str, img: cv2.Mat, ext: str = ".png", params: Sequence[int] = None) -> None:
    """
    Write an image to a file.

    Parameters:
        filename (str): The path to the image file.
        img (cv2.Mat): The image data to be written.
        ext (str, optional): The file extension. Default is ".png".
        params (Sequence[int], optional): Additional parameters for encoding the image. Default is None.

    Returns:
        None: This function does not return any value. It writes the image data to the specified file.

    Example:
        img = imread("image.jpg")
        imwirte("image", img)
    """
    if params:
        cv2.imencode(ext, img, params)[1].tofile(filename)
    else:
        cv2.imencode(ext, img)[1].tofile(filename)


def imshow(img: cv2.Mat, winname: str = "", wait=True) -> None:
    """
    Display an image in a window.

    Parameters:
        img (cv2.Mat): The image data to be displayed.
        winname (str, optional): The name of the window. Default is an empty string.
        wait (bool, optional): Whether to wait for a key press before closing the window. Default is True.

    Returns:
        None: This function does not return any value. It displays the image data in the specified window.

    Example:
        image = imread("image.jpg")
        imshow(image)
    """
    cv2.imshow(winname, img)
    if wait:
        cv2.waitKey(0)


def line(img: cv2.Mat, pt1, pt2, color=DEFAULT_COLOR, thickness: int = DEFAULT_THICKNESS, line_type: int = DEFAULT_LINE_TYPE, shift: int = DEFAULT_SHIFT):
    """
    Draws a line segment connecting two points on an image.

    Parameters:
        img (cv2.Mat): The input image on which the line will be drawn.
        pt1 (tuple): The coordinates of the first point (x1, y1).
        pt2 (tuple): The coordinates of the second point (x2, y2).
        color (tuple, optional): The color of the line in BGR format. Default is DEFAULT_COLOR (red).
        thickness (int, optional): The thickness of the line. Default is DEFAULT_THICKNESS (1).
        line_type (int, optional): The type of the line. Default is DEFAULT_LINE_TYPE (cv2.LINE_AA).
        shift (int, optional): The number of fractional bits in the point coordinates. Default is DEFAULT_SHIFT (0).

    Returns:
        cv2.Mat: The image with the line drawn on it.

    Example:
        line(img,(0,0),(100,100),"#112233") # 在img上画一条从0,0到100,100像素点的颜色为"#112233"的线
    """
    if isinstance(color, str):
        bgr = Colors.colorStrTobgr(color)
    elif isinstance(color, int):
        bgr = Colors.colorStrTobgr(Colors.toString(color))
    else:
        bgr = color
    return cv2.line(img, pt1, pt2, bgr, thickness, line_type, shift)


def rectangle(img: cv2.Mat, pt1, pt2, color=DEFAULT_COLOR, thickness: int = DEFAULT_THICKNESS, line_type: int = DEFAULT_LINE_TYPE, shift: int = DEFAULT_SHIFT):
    """
    Draws a rectangle on an image.

    Parameters:
        img (cv2.Mat): The input image on which the rectangle will be drawn.
        pt1 (tuple): The coordinates of the top-left corner of the rectangle (x1, y1).
        pt2 (tuple): The coordinates of the bottom-right corner of the rectangle (x2, y2).
        color (tuple, optional): The color of the rectangle in BGR format. Default is DEFAULT_COLOR (red).
        thickness (int, optional): The thickness of the rectangle. Default is DEFAULT_THICKNESS (1).
        line_type (int, optional): The type of the line. Default is DEFAULT_LINE_TYPE (cv2.LINE_AA).
        shift (int, optional): The number of fractional bits in the point coordinates. Default is DEFAULT_SHIFT (0).

    Returns:
        cv2.Mat: The image with the rectangle drawn on it.

    Example:
        rectangle(img, (0,0),(100,100))# 在一个img图像上画一个方框,方框左上角坐标为(0,0),右下角坐标为(100,100)
    """
    if isinstance(color, str):
        bgr = Colors.colorStrTobgr(color)
    elif isinstance(color, int):
        bgr = Colors.colorStrTobgr(Colors.toString(color))
    else:
        bgr = color
    return cv2.rectangle(img, pt1, pt2, bgr, thickness, line_type, shift)


def put_text(img: cv2.Mat, text: str, org, font_face=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=DEFAULT_COLOR, thickness: int = DEFAULT_THICKNESS, line_type: int = DEFAULT_LINE_TYPE, bottom_left_origin=False):
    if isinstance(color, str):
        bgr = Colors.colorStrTobgr(color)
    elif isinstance(color, int):
        bgr = Colors.colorStrTobgr(Colors.toString(color))
    else:
        bgr = color
    #TODO: 支持中文绘制
    cv2.putText(img, text, org, font_face, font_scale, bgr,
                thickness, line_type, bottom_left_origin)


def get_pixel(img: cv2.Mat, x: int, y: int) -> str:
    """
    Retrieves the color of a specific pixel in an image.

    Parameters:
        img (cv2.Mat): The input image in OpenCV format.
        x (int): The x-coordinate of the pixel.
        y (int): The y-coordinate of the pixel.

    Returns:
        str: The color of the pixel in hexadecimal format, e.g., "#RRGGBB".
    """
    b, g, r = img[y, x]
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def get_width(img: cv2.Mat):
    return img.shape[1]


def get_height(img: cv2.Mat):
    return img.shape[0]


def clip(img: cv2.Mat, x: int, y: int, w: int, h: int):
    """
    Clips a rectangular region from an input image.

    Parameters:
        img (cv2.Mat): The input image from which to clip the region.
        x (int): The x-coordinate of the top-left corner of the rectangular region.
        y (int): The y-coordinate of the top-left corner of the rectangular region.
        w (int): The width of the rectangular region.
        h (int): The height of the rectangular region.

    Returns:
        cv2.Mat: The clipped rectangular region from the input image.

    Raises:
        ValueError: If the specified region extends beyond the boundaries of the input image.

    Example:
        clip(img,0,0,100,100)# 从img上裁切0,0开始宽为100,高为100的图像
    """
    check_region(img, x + w, y + h)
    return img[y:y+h, x:x+w]


def resize(src: cv2.Mat, dsize, interpolation=cv2.INTER_LINEAR) -> cv2.Mat:
    """
    Resizes an input image to the specified size using the specified interpolation method.

    Parameters:
        src (cv2.Mat): The input image in OpenCV format.
        dsize (tuple): The desired size of the output image as (width, height).
        interpolation (int, optional): The interpolation method to be used. Default is cv2.INTER_LINEAR.

    Returns:
        cv2.Mat: The resized output image in OpenCV format.

    Example:
        resize(img,(100,100))#将图像大小调整为100x100
    """
    return cv2.resize(src, dsize, interpolation=interpolation)


def scale(src: cv2.Mat, fx: int = 1, fy: int = 1, interpolation=cv2.INTER_LINEAR) -> cv2.Mat:
    """
    Resizes an input image by the specified scaling factors using the specified interpolation method.

    Parameters:
        src (cv2.Mat): The input image in OpenCV format.
        fx (int, optional): The scaling factor along the x-axis. Default is 1.
        fy (int, optional): The scaling factor along the y-axis. Default is 1.
        interpolation (int, optional): The interpolation method to be used. Default is cv2.INTER_LINEAR.

    Returns:
        cv2.Mat: The resized output image in OpenCV format.

    Example:
        scale(img,0.8,0.5)#将图像的宽缩放成0.8倍,高缩放成0.5倍
    """
    return cv2.resize(src, None, fx, fy, interpolation)


def cvt_color(src, code):
    return cv2.cvtColor(src, code)


def rgb2bgr(src: cv2.Mat):
    return cv2.cvtColor(src, cv2.COLOR_RGB2BGR)


# def grayscale(src: cv2.Mat) -> cv2.Mat:
#     """
#     Converts an input image from color to grayscale.

#     Parameters:
#         src (cv2.Mat): The input image in OpenCV format. The image should be in BGR color space.

#     Returns:
#         cv2.Mat: The grayscale output image in OpenCV format. The image will be in single-channel (grayscale) color space.

#     Note:
#         If the input image is already in grayscale, the function will return the input image as is.
#     """
#     if src.shape == 2:
#         # The input image is already in grayscale, so return it as is.
#         return src
#     #TODO: 判断当前图像颜色格式
#     # Convert the input image from BGR color space to grayscale using OpenCV's cvtColor function.
#     return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


def threshold(src: cv2.Mat, thresh: float, max_val: float = 255, threshold_type=cv2.THRESH_BINARY):
    return cv2.threshold(src, thresh, max_val, threshold_type)


# TODO: 优化自适应阈值
# def adaptiveThreshold(src: cv2.Mat, maxValue: float, blockSize: int, C: float, adaptiveMethod: int = cv2.MEAN_C, thresholdType: int = cv2.THRESH_BINARY):
#     return cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C)

def select_pyramid_level(img, template):
    min_dim = min(img.shape[0], img.shape[1],
                  template.shape[0], template.shape[1])
    if min_dim < 32:
        return 0
    max_level = int(math.log2(min_dim // 16))
    return min(6, max_level)


def generate_pyramid(img, level):
    pyramid = [img]
    for _ in range(level):
        img = cv2.pyrDown(img)
        pyramid.append(img)
    return pyramid


def find_matches(res, match_threshold):
    loc = np.where(res >= match_threshold)
    return [pt for pt in zip(*loc[::-1])]


def transparent_to_mask(img, alphaThreshold=127):
    if img.shape[2] != 4:
        raise ValueError("Create Mask Must Be BGRA Or RGBA")
    alpha = img[:, :, 3]
    # 透明度阈值设置成127,透明度超过127的将设置成1,否则设置成0，255表示透明，0代表不透明
    _, mask = threshold(alpha, alphaThreshold, 1)
    return mask


def match_template(img, template, region=None, match_threshold=0.95, max_result=5, method=cv2.TM_CCOEFF_NORMED):
    """
    This function performs template matching on an input image and a template image.
    It finds the best matches within the specified region and returns their coordinates.

    Parameters:
        img (cv2.Mat): The input image in OpenCV format.
        template (cv2.Mat): The template image to be matched.
        region (tuple, optional): The region of interest within the input image.The format is (x, y, width, height). Default is the entire image.
        match_threshold (float, optional): The minimum correlation coefficient for a match to be considered valid.Default is 0.95.
        max_result (int, optional): The maximum number of matches to return. Default is 5.
        method (int, optional): The matching method to be used.Default is cv2.TM_CCOEFF_NORMED.

    Returns:
        matches (list): A list of coordinates (x, y) of the best matches found within the specified region.
        If no matches are found, an empty list is returned.

    Example:
        matches =  matchTemplate(img, template)(
        if(len(matches)==0):
            print("No matches found.")
        else:
            print("Matches found:", matches)
    """
    # 设置查找区域
    x, y, w, h = region or (0, 0, img.shape[1], img.shape[0])
    img = clip(img, x, y, w, h)
    # 为带A通道的template创建掩膜
    # TODO: 待测试
    mask = transparent_to_mask(template) if img.shape[2] != 4 else None
    # # 对图像和模板进行灰度化
    # img = grayscale(img)
    # template = grayscale(template)

    matches = []
    res = cv2.matchTemplate(
        img, template, method, mask=mask) if mask else cv2.matchTemplate(img, template, method)

    loc = find_matches(res, match_threshold)

    for pt in loc[:max_result]:
        match = [pt[0] + x, pt[1] + y]
        if not any(np.allclose(match, m) for m in matches):
            matches.append(match)

    return matches


def match_template_best(img, template, region=None, match_threshold=0.95, level=None, method=cv2.TM_CCOEFF_NORMED):
    """
    This function performs template matching on an input image and a template image.
    It finds the best matches within the specified region and returns their coordinates.

    Parameters:
        img (cv2.Mat): The input image in OpenCV format.
        template (cv2.Mat): The template image to be matched.
        region (tuple, optional): The region of interest within the input image. The format is (x, y, width, height). Default is the entire image.
        match_threshold (float, optional): The minimum correlation coefficient for a match to be considered valid. Default is 0.95.
        level (int, optional): The level of the image pyramid to use for matching. Default is None, which means the level is automatically selected.
        method (int, optional): The matching method to be used. Default is cv2.TM_CCOEFF_NORMED.

    Returns:
        tuple: The coordinates (x, y) of the best match found within the specified region. If no matches are found, None is returned.
    """
    # 设置查找区域
    x, y, w, h = region or (0, 0, img.shape[1], img.shape[0])
    img = clip(img, x, y, w, h)

    # 设置金字塔等级
    if level is None:
        level = select_pyramid_level(img, template)

    # # 对图像和模板进行灰度化
    # img = grayscale(img)
    # template = grayscale(template)

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
        res = cv2.matchTemplate(img_level, template_level, method, mask=mask_level) if img.shape[2] == 4 else cv2.matchTemplate(img_level, template_level, method)

        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > match_threshold:
            return max_loc[0] * (2 ** i) + x, max_loc[1] * (2 ** i) + y
    return None


def check_region(img, x, y):
    if img.shape[0] < y or img.shape[1] < x:
        raise ValueError("超出图像边界")
    if 0 > x or 0 > y:
        raise ValueError("超出图像边界")


def find_color_inner(img: cv2.Mat, color: int | str, color_threshold=4, region=None):
    if isinstance(color, str):
        hexColor = int(color[1:], 16)
    elif isinstance(color, int):
        hexColor = color
    else:
        raise ValueError("Color Format Error")
    bgrColor = [hexColor & 0xFF,
                (hexColor >> 8) & 0xFF, (hexColor >> 16) & 0xFF]
    lowerBound = np.array(
        [max(color - color_threshold, 0) for color in bgrColor], dtype=np.uint8
    )
    upperBound = np.array(
        [min(color + color_threshold, 255) for color in bgrColor], dtype=np.uint8
    )
    x, y, w, h = region or [0, 0, img.shape[1], img.shape[0]]
    img = clip(img, x, y, w, h)
    mask = cv2.inRange(img, lowerBound, upperBound)
    return cv2.findNonZero(mask)


def find_color(img: cv2.Mat, color: int | str, region=None, color_threshold=4):
    """
    This function finds the first pixel in an image that matches a specified color within a given region.

    Parameters:
        img (cv2.Mat): The input image in OpenCV format.
        color (int | str): The color to match. This can be specified as an integer value (e.g., 0xFF0000 for red) or as a string value (e.g., "#FF0000" for red).
        region (list, optional): The region within which to search for the matching pixel. This should be specified as a list of four integers: [xmin, ymin, xmax, ymax]. If no region is specified, the entire image will be searched.
        color_threshold (int, optional): The maximum difference allowed between the specified color and the actual color of a pixel for it to be considered a match. Default is 4.

    Returns:
        list: A list containing the x and y coordinates of the first matching pixel. If no matching pixel is found, the function returns None.
    """
    result = find_color_inner(img, color, color_threshold, region)
    if result is None:
        return None
    point = [e for e in result[0][0]]
    return [point[0] + region[0], point[1] + region[1]] if region else point



def find_all_points_color(img: cv2.Mat, color: int | str, region=None, color_threshold=4):
    """
    This function finds all pixels in an image that match a specified color within a given region.

    Parameters:
        img (cv2.Mat): The input image in OpenCV format.
        color (int | str): The color to match. This can be specified as an integer value (e.g., 0xFF0000 for red) or as a string value (e.g., "#FF0000" for red).
        region (list, optional): The region within which to search for the matching pixels. This should be specified as a list of four integers: [xmin, ymin, xmax, ymax]. If no region is specified, the entire image will be searched.
        color_threshold (int, optional): The maximum difference allowed between the specified color and the actual color of a pixel for it to be considered a match. Default is 4.

    Returns:
        list: A list of tuples, where each tuple contains the x and y coordinates of a matching pixel. If no matching pixels are found, the function returns an empty list.
    """
    result = find_color_inner(img, color, color_threshold, region)
    if result is None:
        return None
    points = [(p[0][0], p[0][1]) for p in result]
    return (
        [(point[0] + region[0], point[1] + region[1]) for point in points]
        if region
        else points
    )


def find_multi_colors(img: cv2.Mat, firstColor: int | str, colors, region=None, color_threshold=4):
    """
    This function finds all pixels in an image that match a specified color within a given region.

    Parameters:
        img (cv2.Mat): The input image in OpenCV format.
        firstColor (int | str): The color to match. This can be specified as an integer value (e.g., 0xFF0000 for red) or as a string value (e.g., "#FF0000" for red).
        colors (list): A list of tuples, where each tuple contains the x and y coordinates of a pixel to match and the target color.
        region (list, optional): The region within which to search for the matching pixels. This should be specified as a list of four integers: [xmin, ymin, xmax, ymax]. If no region is specified, the entire image will be searched.
        color_threshold (int, optional): The maximum difference allowed between the specified color and the actual color of a pixel for it to be considered a match. Default is 4.

    Returns:
        tuple: A tuple containing the x and y coordinates of the first matching pixel. If no matching pixels are found, the function returns None.
    """
    firstColorPoints = find_all_points_color(
        img, firstColor, region=region, color_threshold=color_threshold
    )
    if firstColorPoints is None:
        return None
    for x0, y0 in firstColorPoints:
        result = (x0, y0)
        for x, y, target_color in colors:
            if isinstance(target_color, str):
                color = Colors.parseColor(target_color)
            elif isinstance(target_color, int):
                color = target_color
            else:
                raise ValueError("Color Format Error")
            offsetColorStr = get_pixel(img, x + x0, y + y0)
            offsetColor = Colors.parseColor(offsetColorStr)
            if not Colors.isSimilar(color, offsetColor, threshold=color_threshold):
                result = None
                break
        if result is not None:
            return result
    return None


# TODO: 添加特征点匹配


if __name__ == "__main__":
    pass