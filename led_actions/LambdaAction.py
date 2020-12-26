from typing import Union, Iterable, Callable

import neopixel

from Utils.color_util import RGBBytesColor
from led_actions.LedAction import LedAction
from led_actions.NeoPixelWrappers import NeoPixelRange

VoidFn = Callable[[], None]


class LambdaAction(LedAction):
    @classmethod
    def start_and_update(cls, fn: VoidFn) -> "LambdaAction":
        return LambdaAction(fn, fn)

    def __init__(self, start_func: VoidFn, update_func: VoidFn):
        super(LambdaAction, self).__init__(None, float("inf"))
        self.start_fn = start_func
        self.update_fn = update_func

    def _start(self, t: float):
        if self.start_fn:
            self.start_fn()

    def _update(self, t: float, dt: float):
        if self.update_fn:
            self.update_fn()
