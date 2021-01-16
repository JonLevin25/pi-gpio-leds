from enum import Enum
from typing import Callable

from Utils.misc_util import FnVoid
from led_actions.Basic.LedAction import LedAction

class LambdaActionRunMode(Enum):
    StartAndUpdate = 0,
    UpdateOnly = 1,
    StartOnly = 2,

class LambdaAction(LedAction):
    @classmethod
    def from_function(cls, fn: FnVoid, run_mode: LambdaActionRunMode = LambdaActionRunMode.StartAndUpdate):
        update_fn = None if run_mode == LambdaActionRunMode.StartOnly else fn
        start_fn = None if run_mode == LambdaActionRunMode.UpdateOnly else fn
        return LambdaAction(start_fn, update_fn)

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
