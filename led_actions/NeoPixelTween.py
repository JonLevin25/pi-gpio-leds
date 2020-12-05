from typing import Union

from neopixel import NeoPixel
from led_actions.NeoPixelRange import NeoPixelRange
from pytweening import linear

class NeoPixelTween:
    def __init__(self, pixels: Union[NeoPixelRange, NeoPixel], duration: float, easing=linear):
        if duration <= 0:
            raise ValueError("Iteration time muse be positive!")

        self.pixelRange = pixels if isinstance(pixels, NeoPixelRange) else NeoPixelRange(pixels)
        self.duration = duration
        self.easing = easing

    def start(self, curr_time: float):
        self.start_time = curr_time
        self.prev_tick = curr_time
        self._start(curr_time)

    def update(self, curr_time: float):
        dt = curr_time - self.prev_tick
        self._update(curr_time, dt)
        self.prev_tick = curr_time


    def _start(self, start_time: float):
        pass


    def _update(self, dt: float):
        """
        t: the time since start
        dt: the time since last update
        """
        pass