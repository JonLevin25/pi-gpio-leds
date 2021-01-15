import tornado.web as t_web
import tornado.websocket as t_websocket
from tornado.ioloop import IOLoop

import event_loop
from LED_Server.actions.actions_service import ActionsService
from LED_Server.discovery.discovery_service import DiscoveryService
from Utils.ActionsRouter import ActionsRouter
from Utils.PixelsActionsRouter import PixelsActionsRouter
from CONSTS import *
from Utils.color_util import COL_RED



# noinspection PyAbstractClass



def init() -> PixelsActionsRouter:
    pixels = event_loop.init_pixels(30)
    pixels.fill(COL_RED)
    pixels.brightness = 0.3
    pixels.show()

    from LEDActionsHandler import actions_router_ctor
    router = actions_router_ctor(pixels)

    return router


if __name__ == "__main__":
    router = init()
    application = t_web.Application([
        (DISCOVERY_PATH, DiscoveryService, dict(actions_router=router)),
        (ACTIONS_PATH, ActionsService, dict(actions_router=router)),
        # (ACTIONS_PATH, WebSocketHandler, dict(actions_router=router)),
    ])

    application.listen(PORT)
    print(f'listening on port {PORT}')
    IOLoop.current().start()
