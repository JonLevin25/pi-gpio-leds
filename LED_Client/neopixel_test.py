import math
from asyncio.events import AbstractEventLoop
from typing import TypeVar, Generic, Callable

import pytweening
import board
import neopixel
import time
import asyncio

# Colors
COL_BLACK = (0, 0, 0)
COL_BLUE = (0, 255, 0)
COL_RED = (255, 0, 0)

pixels = neopixel.NeoPixel(board.D18, 25, brightness=0.1)

pixels.fill(COL_BLACK)
pixels.show()


def inverse_lerp(t: float, from_: float, to: float) -> float:
    delta = to - from_
    if delta == 0:
        raise ValueError("_from and to cannot be the same!")
    return (t - from_) / delta


def lerp(t: float, from_: float, to: float) -> float:
    delta = to - from_
    return from_ + t * delta


T = TypeVar('T')


class TempBase(Generic[T]):
    def __init__(self, iteration_time: float, ):
        if iteration_time <= 0:
            raise ValueError("Iteration time muse be positive!")

        self.iteration_time = iteration_time

    def _tick(self, curr_time: float):
        normalized_t = (curr_time - self.begin_time) / self.iteration_time
        normalized_dt = (curr_time - self.prev_tick) / self.iteration_time
        self.update(normalized_dt)
        self.prev_tick = curr_time

    def run(self, curr_time: float):
        self.begin_time = curr_time
        self.prev_tick = curr_time
        self.start(curr_time)

    def start(self, start_time: float):
        pass

    def update(self, dt: float):
        """
        t: the normalized time since start
        dt: the normalized time since last tick
        """
        pass


class BrightnessPingPong(TempBase):
    def __init__(self, half_cycle_time: float, min_brightness: float, max_brightness: float, start_ascending=True,
                 ease_func: Callable[[float], float]=pytweening.linear):
        MIN_ALLOWED_BRIGHTNESS = 0.0
        MAX_ALLOWED_BRIGHTNESS = 0.99 # to avoid getting stuck

        super().__init__(half_cycle_time)
        self.min_brightness = max(min_brightness, MIN_ALLOWED_BRIGHTNESS)
        self.max_brightness = min(max_brightness, MAX_ALLOWED_BRIGHTNESS)
        self.start_ascending = start_ascending
        self.ease_func = ease_func

    def clamp_brightness(self, b: float) -> float:
        return max(min(b, self.max_brightness), self.min_brightness)

    def get_brightness(self) -> float:
        return pixels.brightness

    def set_brightness(self, val: float):
        pixels.brightness = val

    def get_normalized_t(self, t: float):
        norm_t_unclamped = (t - self.start_time) / self.iteration_time + self.norm_offset
        complete_iters = int(norm_t_unclamped)
        curr_ascending = self.start_ascending ^ complete_iters % 2  # true if currently ascending

        naive_norm_t = norm_t_unclamped % 1
        return naive_norm_t if curr_ascending else 1 - naive_norm_t

    def get_b(self, norm_t: float) -> float:
        eased_t = self.ease_func(norm_t)
        b = lerp(eased_t, self.min_brightness, self.max_brightness)
        return self.clamp_brightness(b)


    def start(self, t):
        self.start_time = t
        self.norm_offset = inverse_lerp(self.get_brightness(), self.min_brightness, self.max_brightness)

    def update(self, t: float):
        curr_b = self.get_brightness()

        norm_t = self.get_normalized_t(t)
        new_b = self.get_b(norm_t)
        # print('Asc: {}, t: {}, curr_b: {}, new_b: {}, clamped: {}. Range[{}, {}]'.format(self.ascending, t, curr_b, new_b, clamped_new_b, self.min_brightness, self.max_brightness))
        print('norm_t: {:.3f}, new_b: {:.3f}'.format(norm_t, new_b))
        pixels.brightness = new_b
        pixels.show()


def main():
    pixels.brightness = 0
    pixels.fill(COL_BLUE)
    # brightnessPingPong(0, 1, start_ascending=True)

    b = BrightnessPingPong(half_cycle_time=1.5, min_brightness=0.0, max_brightness=1.0, ease_func=pytweening.easeInOutCubic)

    start_time = time.time()
    b.run(start_time)

    prev_time = start_time
    while True:
        curr_time = time.time()
        # b.update(curr_time - prev_time)
        b.update(curr_time)
        prev_time = curr_time


try:
    main()
finally:
    pixels.fill(COL_BLACK)
    pixels.show()
