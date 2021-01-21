import asyncio
import unittest

from tornado.ioloop import IOLoop
from tornado.testing import AsyncTestCase, gen_test

from LED_Server.event_loop import event_loop
from LED_Server.actions.action_routers.PixelsActionsRouter import PixelsActionsRouter
from LED_Server.event_loop.event_loop import FRAME_LENGTH
from led_actions.base.LedAction import LedAction


# todo: extract this to common file somewhere
class TestAction(LedAction):
    # noinspection PyMissingConstructor
    def __init__(self):
        self.started = False
        self.update_count = 0
    def _start(self, start_time: float):
        self.started = start_time
    def _update(self, t: float, dt: float):
        if self.update_count is None:
            self.update_count = 0
        else:
            self.update_count += 1


class MyTestCase(AsyncTestCase):
    def get_new_ioloop(self) -> IOLoop:
        return event_loop.get_ioloop()

    @gen_test
    def test_event_loop_updates_router_running_actions(self):
        # TODO: add OnDestroy, test it as well?
        router = PixelsActionsRouter(None, {'idontcareaboutthis': lambda: None})

        test_action = TestAction()

        router.running_actions = [test_action] # add action directly so no side effects occur

        self.assertFalse(test_action.started)
        self.assertEqual(0, test_action.update_count)

        event_loop.start_pixels_event_loop(router, show_func=lambda: None) # hack so it doesnt try to show pixels

        self.assertEqual(0, test_action.update_count)
        yield asyncio.sleep(FRAME_LENGTH)
        self.assertEqual(1, test_action.update_count)
        yield asyncio.sleep(FRAME_LENGTH)
        self.assertEqual(2, test_action.update_count)

        router.running_actions.remove(test_action)
        yield asyncio.sleep(FRAME_LENGTH)
        self.assertEqual(2, test_action.update_count)



if __name__ == '__main__':
    unittest.main()
