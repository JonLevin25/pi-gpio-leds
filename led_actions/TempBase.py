from typing import List

import neopixel


# TODO: Convert to generic "Tween" / "LedAction" class
class TempBase:
    def __init__(self, pixels: List[neopixel.NeoPixel], iteration_time: float):
        if iteration_time <= 0:
            raise ValueError("Iteration time muse be positive!")

        self.pixels = pixels
        self.iteration_time = iteration_time
        self.norm_t_offset = 0

    def tick(self, curr_time: float):
        dt = curr_time - self.prev_tick
        self._update(curr_time, dt)
        self.prev_tick = curr_time

    def run(self, curr_time: float):
        self.start_time = curr_time
        self.prev_tick = curr_time
        self._start(curr_time)

    @property
    def norm_t_offset(self) -> float:
        return self._norm_t_offset

    @norm_t_offset.setter
    def norm_t_offset(self, value: float):
        self._norm_t_offset = value

    def get_norm_t(self, t: float):
        norm_t_unclamped = (t - self.start_time) / self.iteration_time + self.norm_t_offset
        return norm_t_unclamped % 1

    def get_norm_dt(self, dt: float):
        return dt / self.iteration_time

    def _start(self, start_time: float):
        pass

    def _update(self, t: float, dt: float):
        """
        t: the time since start
        dt: the time since last update
        """
        pass


class TempBasePingPong(TempBase):
    def get_norm_t_pingpong(self, t: float):
        norm_t_unclamped = (t - self.start_time) / self.iteration_time + self.norm_t_offset
        complete_iters = int(norm_t_unclamped)
        curr_ascending = self.start_ascending ^ complete_iters % 2  # true if currently ascending

        naive_norm_t = norm_t_unclamped % 1
        return naive_norm_t if curr_ascending else 1 - naive_norm_t
