import tornado

from Utils.ActionsRouter import ActionsRouter


class WebSocketHandler(tornado.web.WebSocketHandler):
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