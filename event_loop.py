import time
from typing import List

import board
from neopixel import NeoPixel

from Utils.color_util import *
from led_actions.Basic.LedAction import LedAction
from led_actions.Basic.NeoPixelWrappers import NeoPixelRange


def init_pixels(led_count: int) -> NeoPixel:
    ADDRESSABLE_LEDS = led_count  # (30/m * 5m) / 3 [Addr is Groups of 3]
    print('Setting up neopixel + clearing lights')

    pixels = NeoPixel(board.D18, ADDRESSABLE_LEDS, brightness=1, auto_write=False, pixel_order="BRG")
    pixels.fill(COL_BLACK)
    pixels.show()

    return pixels

def run_loop(pixels, actions: List[LedAction]):
    print('{} actions set. Initializing'.format(len(actions)))

    curr_time = time.time()

    # while True:
    #     col = rand_deep_color(lum=1.0)
    #     color_chase(pixels, col, pix_wait=0.001, cycle_wait=0.5)

    for a in actions:
        a.run(curr_time)

    pixels.show()

    print('actions initiazlied')
    while True:
        curr_time = time.time()
        for a in actions:
            a.tick(curr_time)
        pixels.show()
        time.sleep(0.001)  # without this dt is sometimes too small