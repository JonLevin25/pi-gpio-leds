from typing import List

from neopixel import NeoPixel

from Utils.reflection_builder import InvalidParamErrorMode
from Utils.ActionsRouter import ActionsRouter


class PixelsActionsRouter(ActionsRouter):
    '''A simple ActionsRouter that injects "pixels" as the first arg to actions'''
    def __init__(self, pixels: NeoPixel, scheme='(.*?):(.*)$', actions={}):
        self.pixels = pixels
        super(PixelsActionsRouter, self).__init__(scheme, actions)

    def do_action(self, fn_handler, params):
        fn_handler(self.pixels, *params)
        self.pixels.show()

    def get_metadata(self, supported_types: List[type], omitted_types: List[type] = [NeoPixel],
                     on_invalid_params: InvalidParamErrorMode = InvalidParamErrorMode.OMIT_ACTION):
        return super(PixelsActionsRouter, self).get_metadata(supported_types, omitted_types, on_invalid_params)