import tornado.web
from tornado.ioloop import IOLoop

import event_loop
from LED_Server.actions.actions_service import ActionsService
from LED_Server.discovery.discovery_service import DiscoveryService
from CONSTS import *
from Utils.color_util import COL_RED

from LEDActionsHandler import *


def init() -> PixelsActionsRouter:
    pixels = event_loop.init_pixels(30)
    pixels.fill(COL_RED)
    pixels.brightness = 0.3
    pixels.show()

    router = PixelsActionsRouter(pixels, {
        'brightness': set_brightness,
        'rand_color': test_fill_rand,
        'set_sequential': Actions_Basic.set_sequential,
        'color_cycle': Actions_ColorCycle.colorcylce,
    })

    return router

if __name__ == "__main__":
    router = init()
    application = tornado.web.Application([
        (DISCOVERY_PATH, DiscoveryService, dict(actions_router=router)),
        (ACTIONS_PATH, ActionsService, dict(actions_router=router)),
        # (ACTIONS_PATH, WebSocketHandler, dict(actions_router=router)),
    ])

    application.listen(PORT)
    print(f'listening on port {PORT}')
    ioloop = IOLoop.current()
    ioloop.run_sync(lambda: event_loop.run_loop(router.pixels, router.running_actions))
    ioloop.start()

