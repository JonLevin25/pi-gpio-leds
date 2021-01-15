import json
from typing import Optional, Awaitable

import tornado.web

# TODO: "Discover" get route that returns the signatures (key + param types (names?) of everything in actions_router
from Utils.ActionsRouter import ActionsRouter


# noinspection PyAbstractClass
class DiscoveryService(tornado.web.RequestHandler):
    # noinspection PyAttributeOutsideInit
    def initialize(self, actions_router: ActionsRouter) -> None:
        self.actions_router = actions_router

    def get(self):
        print("Handling Discovery request")
        metadata = self.actions_router.get_metadata()
        json_meta = json.dumps(metadata)
        self.write(json_meta)
