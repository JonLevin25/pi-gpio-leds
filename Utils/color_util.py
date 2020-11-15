from typing import Iterable

from colorzero.conversions import hsv_to_rgb, rgb_to_hsv
from random import random

# Colors
COL_BLACK = (0, 0, 0)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_BLUE = (0, 0, 255)


def get_hsv(rgb_bytes: Iterable[int]) -> Iterable[float]:
    return rgb_to_hsv(*(x / 255 for x in rgb_bytes))


def get_hue(rgb_bytes: Iterable[int]) -> float:
    hsv = get_hsv(rgb_bytes)
    return hsv.hue


# TODO: get light from pixels.brightness
def get_rgb_bytes(hue: float, sat: float = 1, light: float = 1):
    rgb = hsv_to_rgb(hue, sat, light)
    return [int(x * 255) for x in rgb]


def add_hue(rgb_bytes: Iterable[int], hue_to_add: float):
    old_hue = get_hue(rgb_bytes)
    rgb_bytes = get_rgb_bytes(old_hue + hue_to_add)
    return rgb_bytes


def rand_color():
    hue = random()
    return get_rgb_bytes(hue)
