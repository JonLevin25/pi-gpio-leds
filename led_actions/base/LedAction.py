from typing import List, Callable
import uuid

import neopixel


# TODO: Convert to generic "Tween" / "LedAction" class
from Utils.misc_util import FnVoid


class LedAction:
    def __init__(self, pixels: neopixel.NeoPixel, iteration_time: float):
        if iteration_time <= 0:
            raise ValueError("Iteration time muse be positive!")

        self.pixels = pixels
        self.iteration_time = iteration_time
        self.norm_t_offset = 0
        self._enabled = True
        self._didstart = False
        self._destroyed = False
        self.uuid = str(uuid.uuid4())[9:18]

        self.destroy_callbacks = set()

    def subscribe_to_destroy(self, callback: Callable[["LedAction"], None]):
        if not callback: return
        self.destroy_callbacks.add(callback)

    # TODO: TEST THIS WORKS! (set able to find function? no hash collisions?)
    def unsubscribe_to_destroy(self, callback: FnVoid):
        self.destroy_callbacks.add(callback)

    #this doesnt remove memory, but marks as destroyed. relies on ActionRouter removing it for garbage collection
    def destroy(self):
        self.enabled = False
        self._destroyed = True

        for callback in self.destroy_callbacks:
            callback(self)

    def __repr__(self):
        return f'<{type(self).__name__} {self.uuid}>'

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

        # TODO: autostart on enable (Requires Time DI/global config)
        # if value and not self._didstart:
        #     self._start(Time.now)

    def toggle_enabled(self):
        self.enabled = not self.enabled
        return self.enabled

    def tick(self, curr_time: float):
        if self._destroyed or not self.enabled:
            return

        dt = curr_time - self.prev_tick
        self._update(curr_time, dt)
        self.prev_tick = curr_time

    def run(self, curr_time: float):
        self.start_time = curr_time
        self.prev_tick = curr_time

        if not self.enabled:
            return

        self._start(curr_time)
        self._didstart = True

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
