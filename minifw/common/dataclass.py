from dataclasses import dataclass


@dataclass
class Point:
    x:int
    y:int

@dataclass
class Rect:
    x:int
    y:int
    w:int
    h:int

@dataclass
class RGB:
    r:int
    g:int
    b:int

@dataclass
class LAB:
    l:float
    a:float
    b:float

@dataclass
class HSV:
    h:float
    s:float
    v:float

@dataclass
class ImageSize:
    width:int
    height:int