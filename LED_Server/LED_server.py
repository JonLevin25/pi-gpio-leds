import tornado.web as t_web
import tornado.websocket as t_websocket
from tornado.ioloop import IOLoop
from TestActionsHandler import actions_router

ROUTE = r"/leds"


class WebSocketHandler(t_websocket.WebSocketHandler):
    def open(self):
        print("New client connected")
        self.write_message("You are connected")


    def on_message(self, message):
        if type(message) == bytes:
            self.write_and_err("Expected string message, but received bytes!")
            return
        self.write_and_log(message)
        actions_router.handle(message)

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


application = t_web.Application([
    (ROUTE, WebSocketHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    IOLoop.current().start()

