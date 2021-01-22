import logging
from typing import List, Mapping, Callable, Iterable, Union

from neopixel import NeoPixel

from LED_Server.actions.action_routers.ActionsRouter import ActionsRouter
from LED_Server.models.action_models import ActionRequestParam
from Utils.time_util import Time
from led_actions.base.LedAction import LedAction

PixelActionFn = Callable[..., Union[LedAction, None]]

class PixelsActionsRouter(ActionsRouter):
    '''A simple ActionsRouter that injects "pixels" to args'''

    def __init__(self, pixels: NeoPixel, action_map: Mapping[str, Callable]):
        self.pixels = pixels
        self.running_actions = []
        super().__init__(action_map, supported_types=[int, float, str], closure_params={'pixels': pixels})

    def call_function(self, fn: PixelActionFn, params: List['ActionRequestParam']):
        fn_result = super(PixelsActionsRouter, self).call_function(fn, params)

        # if its a LedAction - run it exclusively for now
        if isinstance(fn_result, LedAction):
            self.clear_running_actions()
            self.add_action(fn_result)
        self.pixels.show()

    def add_actions(self, actions: Iterable[LedAction]):
        for action in actions:
            self.add_action(action)

    def add_action(self, action: LedAction):
        if action is None:
            logging.error('action was None!')
            return
        action.run(Time.now())
        self.running_actions.append(action)

    def clear_running_actions(self):
        self.running_actions.clear()  # dont replace list (actions = []) - since ref is used by event loop
