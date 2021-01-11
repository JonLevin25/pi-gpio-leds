from typing import Iterable, List, Tuple, Union, Callable

from colorzero.conversions import hsv_to_rgb, rgb_to_hsv, html_to_rgb_bytes
from random import random

RGBBytesColor = Union[Tuple[int, int, int], List[int]]
HSVColor = Union[Tuple[float, float, float], List[float]]

ColorGetter = Callable[[], RGBBytesColor]

# Colors
COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_BLUE = (0, 0, 255)


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
