from typing import Iterable, List, Tuple, Union, Callable

from colorzero.conversions import hsv_to_rgb, rgb_to_hsv, html_to_rgb_bytes
from random import random

from Utils.math_util import clampInt, mapTo, lerpInt

RGBBytesColor = Union[Tuple[int, int, int], List[int]]
HSVColor = Union[Tuple[float, float, float], List[float]]

ColorGetter = Callable[[], RGBBytesColor]

# Colors
COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_BLUE = (0, 0, 255)

def color_lerp_hsv(t: float, from_col: RGBBytesColor, to_col: RGBBytesColor):
    f_h, f_s, f_l = get_hsv(from_col)
    t_h, t_s, t_l = get_hsv(to_col)

    posdelta = t_h - f_h
    negdelta = -(256-t_h) - f_h
    if abs(negdelta) < abs(posdelta):
        t_h -= 256

    h = mapTo(t, (0, 1), (f_h, t_h))
    s = mapTo(t, (0, 1), (f_s, t_s))
    l = mapTo(t, (0, 1), (f_l, t_l))

    if (h < 0):
        h += 256
    return get_rgb_bytes(h, s, l)


def color_lerp_rgb(t: float, from_col: RGBBytesColor, to_col: RGBBytesColor):
    f_r, f_g, f_b = from_col
    t_r, t_g, t_b = to_col

    raw_r = lerpInt(t, f_r, t_r)
    raw_g = lerpInt(t, f_g, t_g)
    raw_b = lerpInt(t, f_b, t_b)

    r = clampInt(raw_r, 0, 255)
    g = clampInt(raw_g, 0, 255)
    b = clampInt(raw_b, 0, 255)

    return (r, g, b)

def get_hsv(rgb_bytes: RGBBytesColor) -> HSVColor:
    return rgb_to_hsv(*(x / 255 for x in rgb_bytes))


def get_hue(rgb_bytes: RGBBytesColor) -> float:
    hsv = get_hsv(rgb_bytes)
    return hsv.hue

# TODO: get light from pixels.brightness
def get_rgb_bytes(hue: float, sat: float = 1, light: float = 1) -> RGBBytesColor:
    rgb = hsv_to_rgb(hue, sat, light)
    return [int(x * 255) for x in rgb]


def add_hue(rgb_bytes: RGBBytesColor, hue_to_add: float) -> RGBBytesColor:
    old_hue = get_hue(rgb_bytes)
    rgb_bytes = get_rgb_bytes(old_hue + hue_to_add)
    return rgb_bytes


def rand_color() -> RGBBytesColor:
    hue = random()
    return get_rgb_bytes(hue)
