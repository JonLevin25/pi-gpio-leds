from led_actions.base.LedAction import LedAction


class TestAction(LedAction):
    def __init__(self):
        super(TestAction, self).__init__(None, 1.0)
        self.started = False
        self.update_count = 0
    def _start(self, start_time: float):
        self.started = start_time
    def _update(self, t: float, dt: float):
        if self.update_count is None:
            self.update_count = 0
        else:
            self.update_count += 1