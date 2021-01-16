from typing import Iterable

from led_actions.base.LedAction import LedAction


class ActionQueue(LedAction):
    def __init__(self, actions: Iterable[LedAction]):
        # noinspection PyTypeChecker
        super(ActionQueue, self).__init__(None, float("inf"))
        self.actions = actions if type(actions) == list else list(actions)

    def run(self, t: float):
        super(ActionQueue, self).run(t)
        for action in self.actions:
            action.run(t)

    def tick(self, t: float):
        super(ActionQueue, self).tick(t)
        for action in self.actions:
            action.tick(t)
