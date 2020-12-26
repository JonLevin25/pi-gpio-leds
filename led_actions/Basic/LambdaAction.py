from typing import Callable

from Utils.misc_util import FnVoid
from led_actions.Basic.LedAction import LedAction


class LambdaAction(LedAction):
    @classmethod
    def start_and_update(cls, fn: FnVoid) -> "LambdaAction":
        return LambdaAction(fn, fn)

    def __init__(self, start_func: FnVoid, update_func: FnVoid):
        super(LambdaAction, self).__init__(None, float("inf"))
        self.start_fn = start_func
        self.update_fn = update_func

    def _start(self, t: float):
        if self.start_fn:
            self.start_fn()

    def _update(self, t: float, dt: float):
        if self.update_fn:
            self.update_fn()
