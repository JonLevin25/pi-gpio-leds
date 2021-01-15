from typing import List, Mapping, Callable

from neopixel import NeoPixel

from Utils.reflection_builder import InvalidParamErrorMode
from Utils.ActionsRouter import ActionsRouter, ActionRequestParam


class PixelsActionsRouter(ActionsRouter):
    '''A simple ActionsRouter that injects "pixels" to args'''

    def __init__(self, pixels: NeoPixel, actions: Mapping[str, Callable]):
        self.pixels = pixels
        super().__init__(actions, supported_types=[int, float, str], closure_params = {'pixels': pixels})

    def _apply(self, fn: Callable[[any], None], params: List['ActionRequestParam']):
        super(PixelsActionsRouter, self)._apply(fn, params)
        self.pixels.show()
