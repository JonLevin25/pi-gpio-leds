from typing import List, Iterable, Union

import neopixel

from Utils.color_util import RGBBytesColor
from Utils.misc_util import is_iter
from led_actions.LedAction import LedAction
from led_actions.NeoPixelWrappers import NeoPixelRange


class SetRangesAction(LedAction):
    def __init__(self, pixels: Union[neopixel.NeoPixel, NeoPixelRange, Iterable[NeoPixelRange]], color: RGBBytesColor):
        # noinspection PyTypeChecker
        super(SetRangesAction, self).__init__(pixels, float("inf"))
        self.color = color

    def _start(self, start_time: float):
        self._apply_color()

    def _update(self, t: float, dt: float):
        self._apply_color()

    def _apply_color(self):
        if isinstance(self.pixels, neopixel.NeoPixel):
            self.pixels.fill(self.color)
            return

        pixels = self.pixels
        pix_ranges = pixels if is_iter(pixels) else [pixels]
        self._set_range(pix_ranges)

    def _set_range(self, pix_ranges: Iterable[NeoPixelRange]):
        for pxrange in pix_ranges:
            pxrange.set_colors(self.color)