import pytweening
import board
import neopixel
import time

from typing import *
from Utils.color_util import *
from Utils.math_util import *
from led_actions.BrightnessPingPongAction import BrightnessPingPong
from led_actions.ColorCycleAction import ColorCycle

ADDRESSABLE_LEDS = 30  # (30/m * 5m) / 3 [Addr is Groups of 3]

print('Setting up neopixel + clearing lights')
pixels = neopixel.NeoPixel(board.D18, ADDRESSABLE_LEDS, brightness=1, auto_write=False)
pixels.fill(COL_BLACK)
pixels.show()


def test_color_cycle():
    while True:
        for i in range(len(pixels)):
            p = pixels[i]
            new_p = add_hue(p, 0.002)
            pixels[i] = new_p
        pixels.show()

        time.sleep(0.0000000001)


# convenience actions, just so its easier to comment lines out in actions set
def action_bright_pingpong():
    return BrightnessPingPong(pixels, half_cycle_time=2.5, min_brightness=0.0, max_brightness=1.0,
                       ease_func=pytweening.easeInOutCubic),


def action_colorcycle():
    return ColorCycle(pixels, 10)


def main():
    test = [rand_color() for i in range(len(pixels))]
    pixels[:] = test
    # pixels.brightness = 0

    print('creating actions to run')
    actions = {
        # action_bright_pingpong(),
        action_colorcycle(),

    }
    print('{} actions set. Initializing'.format(len(actions)))

    curr_time = time.time()
    for a in actions:
        a.run(curr_time)

    pixels.show()

    print('actions initiazlied')
    while True:
        curr_time = time.time()
        for a in actions:
            a.tick(curr_time)
        pixels.show()


try:
    main()
finally:
    print('creating actions to run')
    pixels.fill(COL_BLACK)
    pixels.show()
    print('Exiting...')

