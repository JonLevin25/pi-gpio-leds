import asyncio
import unittest

from tornado.testing import AsyncTestCase, gen_test

from LED_Server.event_loop import event_loop
from LED_Server.actions.action_routers.PixelsActionsRouter import PixelsActionsRouter
from LED_Server.event_loop.event_loop import FRAME_LENGTH
from LED_Server.tests_common.TestAction import TestAction


class MyTestCase(AsyncTestCase):
    @gen_test
    def test_event_loop_updates_router_running_actions(self):
        # TODO: add OnDestroy, test it as well?
        router = PixelsActionsRouter(None, {'idontcareaboutthis': lambda: None})

        test_action = TestAction()

        router.running_actions = [test_action]  # add action directly so no side effects occur

        self.assertFalse(test_action.started)
        self.assertEqual(0, test_action.update_count)

        # show_func is a hack so it doesnt try to show pixels
        lifecycle_coroutine = event_loop.start_pixels_lifecycle_async(router, show_func=lambda router: None)
        asyncio.create_task(lifecycle_coroutine)

        yield  # make sure the event loop executes the first update

        self.assertEqual(1, test_action.update_count)  # start_pixels immediately runs a frame update

        yield asyncio.sleep(FRAME_LENGTH * 0.5)
        self.assertEqual(1, test_action.update_count)
        yield asyncio.sleep(FRAME_LENGTH * 0.7)  # wait a bit longer than a frame cause async
        self.assertEqual(2, test_action.update_count)

        yield asyncio.sleep(FRAME_LENGTH)
        self.assertEqual(3, test_action.update_count)

        # remove action, no more updates
        router.running_actions.remove(test_action)
        yield asyncio.sleep(FRAME_LENGTH * 2)
        self.assertEqual(3, test_action.update_count)


if __name__ == '__main__':
    unittest.main()
