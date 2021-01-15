from neopixel import NeoPixel

from Utils.ActionsRouter import ActionsRouter


class PixelsActionsRouter(ActionsRouter):
    '''A simple ActionsRouter that injects "pixels" as the first arg to actions'''
    def __init__(self, pixels: NeoPixel, scheme='(.*?):(.*)$', actions={}):
        self.pixels = pixels
        super(PixelsActionsRouter, self).__init__(scheme, actions)

    def do_action(self, fn_handler, params):
        fn_handler(self.pixels, *params)
        self.pixels.show()