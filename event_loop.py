import asyncio

import board
from neopixel import NeoPixel
from tornado.ioloop import IOLoop

from LED_Server.actions.action_routers.PixelsActionsRouter import PixelsActionsRouter
from Utils.color_util import *
from Utils.time_util import Time
from led_actions.base.LedAction import LedAction

# TODO: implement proper (awaitable) wait_frame() method instead of exposing this
FRAME_LENGTH = 0.00833  # 120Hz - without this dt is sometimes too small

FnShow = Callable[[PixelsActionsRouter], None]
default_show_fn: FnShow = lambda router: router.pixels.show()

# ugly hack because async tests break and I dont want to add more modules to fix it for now
ioloop_singleton: Union[IOLoop, None] = None

def get_ioloop() -> IOLoop:
    global ioloop_singleton # TODO: Why cant I edit this without global?
    if ioloop_singleton is None:
        ioloop_singleton = IOLoop.current()
    return ioloop_singleton


def init_pixels(led_count: int) -> NeoPixel:
    ADDRESSABLE_LEDS = led_count  # (30/m * 5m) / 3 [Addr is Groups of 3]
    print('Setting up neopixel + clearing lights')

    pixels = NeoPixel(board.D18, ADDRESSABLE_LEDS, brightness=1, auto_write=False, pixel_order="BRG")
    pixels.fill(COL_BLACK)
    pixels.show()

    return pixels


def start_pixels_event_loop(router: PixelsActionsRouter, show_func: FnShow = default_show_fn): # show func just for testing
    ioloop = get_ioloop()
    ioloop.run_sync(lambda: _event_loop(router, show_func))


async def _event_loop(router: PixelsActionsRouter, show_func: FnShow):
    print('{} actions set. Initializing'.format(len(router.running_actions)))

    curr_time = Time.now()
    for a in router.running_actions:
        a.run(curr_time)

    show_func(router)

    print('actions initiazlied')
    while True:
        curr_time = Time.now()
        for a in router.running_actions:
            a.tick(curr_time)
        show_func(router)
        await asyncio.sleep(FRAME_LENGTH)
