import asyncio

import board
from neopixel import NeoPixel
from tornado.ioloop import IOLoop

from LED_Server.actions.action_routers.PixelsActionsRouter import PixelsActionsRouter
from Utils.color_util import *
from Utils.time_util import Time
from led_actions.base.LedAction import LedAction


def init_pixels(led_count: int) -> NeoPixel:
    ADDRESSABLE_LEDS = led_count  # (30/m * 5m) / 3 [Addr is Groups of 3]
    print('Setting up neopixel + clearing lights')

    pixels = NeoPixel(board.D18, ADDRESSABLE_LEDS, brightness=1, auto_write=False, pixel_order="BRG")
    pixels.fill(COL_BLACK)
    pixels.show()

    return pixels


def start_pixels_event_loop(router: PixelsActionsRouter):
    ioloop = IOLoop.current()
    ioloop.run_sync(lambda: _event_loop(router))


async def _event_loop(pixels, router: PixelsActionsRouter):
    print('{} actions set. Initializing'.format(len(router.running_actions)))

    curr_time = Time.now()
    for a in router.running_actions:
        a.run(curr_time)

    pixels.show()

    print('actions initiazlied')
    while True:
        curr_time = Time.now()
        for a in router.running_actions:
            a.tick(curr_time)
        pixels.show()
        await asyncio.sleep(0.00833)  # 120Hz - without this dt is sometimes too small
