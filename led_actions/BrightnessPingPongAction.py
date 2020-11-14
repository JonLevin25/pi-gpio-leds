from typing import Callable

import pytweening

from Utils.math_util import *
from led_actions.LedActionPingPong import LedActionPingPong


# work with deltas so it reacts to outside changes
class BrightnessPingPong(LedActionPingPong):
    def __init__(self, pixels, half_cycle_time: float, min_brightness: float, max_brightness: float,
                 start_ascending=True,
                 ease_func: Callable[[float], float] = pytweening.linear):
        MIN_ALLOWED_BRIGHTNESS = 0.0
        MAX_ALLOWED_BRIGHTNESS = 0.99  # to avoid getting stuck

        super().__init__(pixels=pixels, iteration_time=half_cycle_time)
        self.min_brightness = max(min_brightness, MIN_ALLOWED_BRIGHTNESS)
        self.max_brightness = min(max_brightness, MAX_ALLOWED_BRIGHTNESS)
        self.start_ascending = start_ascending
        self.ease_func = ease_func

    def clamp_brightness(self, b: float) -> float:
        return max(min(b, self.max_brightness), self.min_brightness)

    def get_brightness(self) -> float:
        return self.pixels.brightness

    def set_brightness(self, val: float):
        self.pixels.brightness = val

    def get_b(self, norm_t: float) -> float:
        eased_t = self.ease_func(norm_t)
        b = lerp(eased_t, self.min_brightness, self.max_brightness)
        return self.clamp_brightness(b)

    def _start(self, t):
        self.norm_t_offset = inverse_lerp(self.get_brightness(), self.min_brightness, self.max_brightness)

    def _update(self, t: float, dt: float):
        norm_t = self.get_norm_t_pingpong(t)
        new_b = self.get_b(norm_t)
        # print('Asc: {}, t: {}, curr_b: {}, new_b: {}, clamped: {}. Range[{}, {}]'.format(self.ascending, t, curr_b, new_b, clamped_new_b, self.min_brightness, self.max_brightness))
        print('norm_t: {:.3f}, new_b: {:.3f}'.format(norm_t, new_b))
        self.pixels.brightness = new_b