from typing import *

import neopixel
import pytweening

from Utils.color_util import *
from led_actions.LedAction import LedAction


class ColorCycle(LedAction):
    def __init__(self, pixels: neopixel.NeoPixel, cycle_time: float, ascending=True,
                 ease_func: Callable[[float], float] = pytweening.linear):
        super().__init__(pixels=pixels, iteration_time=cycle_time)
        self.ascending = ascending
        self.ease_func = ease_func
        self.pixels = pixels

    def get_next(self, pixel, dt: float) -> float:
        norm_dt = self.get_norm_dt(dt)
        if not self.ascending:
            norm_dt *= -1

        (old_h, s, v) = get_hsv(pixel)
        naive_new_hue = (old_h + norm_dt) % 1
        new_hue = self.ease_func(naive_new_hue)

        rgb_bytes = get_rgb_bytes(new_hue, s, v)
        return rgb_bytes

    def _start(self, t: float):
        pass

    def _update(self, t: float, dt: float):
        for i in range(len(self.pixels)):
            p = self.pixels[i]
            new_p = self.get_next(p, dt)
            self.pixels[i] = new_p