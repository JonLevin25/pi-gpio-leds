import json
import logging
from json import JSONDecodeError
from typing import List

import tornado.web

from CONSTS import HTTP_Headers
from Utils.ActionsRouter import ActionsRouter, ActionRequest


class ActionsService(tornado.web.RequestHandler):
    # noinspection PyAttributeOutsideInit
    def initialize(self, actions_router: ActionsRouter) -> None:
        self.actions_router = actions_router

    def post(self):
        self.set_header(HTTP_Headers.Key_ContentType, HTTP_Headers.Val_AppJson)
        content_type = self.request.headers[HTTP_Headers.Key_ContentType]
        if content_type != HTTP_Headers.Val_AppJson:
            self.write_and_err(400, f'{HTTP_Headers.Key_ContentType} must be set to "{HTTP_Headers.Val_AppJson}"!')
            return

        jsonBody = self.request.body
        try:
            deserialized_json = json.loads(jsonBody)
            action_request = ActionRequest.fromDecodedJson(deserialized_json)
        except JSONDecodeError:
            self.write_and_err(400, 'Error parsing JSON')
            return

        try:
            self.actions_router.handle(action_request)
        except ValueError:
            self.write_and_err(400, f'Error applying action from request ({jsonBody})')

        # self.write('OK')

    def write_and_log(self, msg):
        self.write("You said: " + msg)
        print("RESPONSE: " + msg)

    def write_and_err(self, code: int, message: str):
        self.write_error(code, message = message)
        print("ERROR: " + message)