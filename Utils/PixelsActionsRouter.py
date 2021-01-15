from typing import List, Mapping, Callable

from neopixel import NeoPixel

from Utils.reflection_builder import InvalidParamErrorMode
from Utils.ActionsRouter import ActionsRouter


class PixelsActionsRouter(ActionsRouter):
    '''A simple ActionsRouter that injects "pixels" to args'''

    def __init__(self, pixels: NeoPixel, actions: Mapping[str, Callable]):
        super().__init__(actions, supported_types=[int, float, str], closure_params = {'pixels': pixels})
