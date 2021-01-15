import tornado.web as t_web
import tornado.websocket as t_websocket
from tornado.ioloop import IOLoop

import event_loop
from Utils.ActionsRouter import ActionsRouter
from Utils.PixelsActionsRouter import PixelsActionsRouter
from CONSTS import ROUTE_PATH, PORT
from Utils.color_util import COL_RED


# TODO: "Discover" get route that returns the signatures (key + param types (names?) of everything in actions_router
class DiscoverHTTPServer(t_web.RequestHandler):
    # noinspection PyAttributeOutsideInit
    def initialize(self, actions_router: ActionsRouter) -> None:
        self.actions_router = actions_router

    # def get()


class WebSocketHandler(t_websocket.WebSocketHandler):
    # noinspection PyAttributeOutsideInit
    def initialize(self, actions_router: ActionsRouter) -> None:
        self.actions_router = actions_router

    def open(self):
        print("New client connected")
        self.write_message("You are connected")

    def on_message(self, message):
        if type(message) == bytes:
            self.write_and_err("Expected string message, but received bytes!")
            return
        self.write_and_log(message)
        self.actions_router.handle(message)

    def on_close(self):
        print("Client disconnected")

    def check_origin(self, origin):
        return True

    def write_and_log(self, msg):
        self.write_message("You said: " + msg)
        print("RESPONSE: " + msg)

    def write_and_err(self, err):
        self.write_error(err)
        print("ERROR: " + err)


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
        (ROUTE_PATH, WebSocketHandler, dict(actions_router=router)),
    ])

    application.listen(PORT)
    print(f'listening on port {PORT}')
    IOLoop.current().start()
