#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio import Future
from CONSTS import REMOTE_URL

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect, WebSocketHandler
import asyncio
import tornado.ioloop
import typing

class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ws = None
        PeriodicCallback(self.keep_alive, 20000).start()

    @gen.coroutine
    def connect(self) -> "Future[WebSocketHandler]":
        print(f"trying to connect to {REMOTE_URL}")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error")
        else:
            print("connected")
            self.run()
            return self.ws

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print("connection closed")
                self.ws = None
                break

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")

# TODO: test this
async def connect_ws() -> WebSocketHandler:
    client = Client(REMOTE_URL, 5)
    return await client.connect()

async def main():
    ws = await connect_ws()
    await ws.write_message("brightness:3,5,")

async def test():
    await asyncio.sleep(5)
    print('whoop')

if __name__ == "__main__":
    # IOLoop.instance().run_sync(main) # tornado method
    asyncio.get_event_loop().run_until_complete(main()) # asyncio method


