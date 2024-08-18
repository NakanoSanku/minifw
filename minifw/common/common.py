from minifw.common.dataclass import Rect,Point


def is_point_in_rect(pt: Point, rect: Rect) -> bool:
    """
    判断点是否在矩形内
    :param pt: Point(x,y)
    :param rect: Rect(x,y,w,h)
    :return: bool
    """
    x, y = pt.x, pt.y
    x_min, y_min, x_max, y_max = rect.x, rect.y, rect.x + rect.w, rect.y + rect.h
    return True if x_min <= x <= x_max and y_min <= y <= y_max else False


def is_rect_in_rect(rect1: Rect, rect2: Rect) -> bool:
    """
    判断矩形1是否在矩形2内
    :param rect1: Rect(x,y,w,h)
    :param rect2: Rect(x,y,w,h)
    :return: bool
    """
    x_min, y_min, x_max, y_max = rect1.x, rect1.y, rect1.x + rect1.w, rect1.y + rect1.h
    return True if is_point_in_rect(Point(x_min, y_min), rect2) and is_point_in_rect(Point(x_max, y_max), rect2) else False

if __name__ == '__main__':
    print(is_point_in_rect(Point(1, 10), Rect(0, 0, 10, 10))) # True
    print(is_point_in_rect(Point(11 ,10), Rect(0, 0, 10, 10))) # False
    print(is_rect_in_rect(Rect(2, 2, 8, 8), Rect(0, 0, 10, 10))) # True
    print(is_point_in_rect(Point(11, 10), Rect(0, 0, 10, 10))) # False