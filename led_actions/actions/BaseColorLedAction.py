from typing import Union

import neopixel

from Utils.color_util import RGBBytesColor
from led_actions.base.LedAction import LedAction
from led_actions.experimental.NeoPixelWrappers import NeoPixelRange


class BaseColorLedAction(LedAction):
    def __init__(self, pixels: Union[neopixel.NeoPixel, NeoPixelRange], color: RGBBytesColor):
        super().__init__(pixels=pixels, iteration_time=1)
        self.pixels = pixels
        self.color = color

    def fill(self):
        self.pixels.fill(self.color)

    def _start(self, t: float):
        self.fill()

    def _update(self, t: float, dt: float):
        self.fill()