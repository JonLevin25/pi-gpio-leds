from typing import List, Mapping, Callable

from neopixel import NeoPixel

from LED_Server.actions.action_routers.ActionsRouter import ActionsRouter
from LED_Server.models.action_models import ActionRequestParam
from Utils.time_util import Time
from led_actions.base.LedAction import LedAction


class PixelsActionsRouter(ActionsRouter):
    '''A simple ActionsRouter that injects "pixels" to args'''

    def __init__(self, pixels: NeoPixel, actions: Mapping[str, Callable]):
        self.pixels = pixels
        self.running_actions = []
        super().__init__(actions, supported_types=[int, float, str], closure_params = {'pixels': pixels})

    def _apply(self, fn: Callable[[any], None], params: List['ActionRequestParam']):
        fn_return = super(PixelsActionsRouter, self)._apply(fn, params)

        # if its a LedAction - run it exclusively for now
        if isinstance(fn_return, LedAction):
            self.stop_running_actions()
            fn_return.run(Time.now())
            self.running_actions.append(fn_return)

        self.pixels.show()

    def stop_running_actions(self):
        self.running_actions.clear() # dont replace list (actions = []) - since ref is used by event loop