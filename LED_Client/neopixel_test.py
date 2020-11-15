import pytweening
import itertools
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


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def set_sequential(pixels: neopixel.NeoPixel, offset: float = 0.0):
    num_pixels = len(pixels)
    for i in range(num_pixels):
        hue = (i / num_pixels) + offset
        pixels[i] = get_rgb_bytes(hue, light=pixels.brightness)


def set_random(pixels: neopixel.NeoPixel):
    test = [rand_color() for i in range(len(pixels))]
    pixels[:] = test


# convenience actions, just so its easier to comment lines out in actions set
def action_bright_pingpong():
    # dont set min brighness to 0 since that messes up hue calculation for other funcs
    return BrightnessPingPong(pixels, half_cycle_time=60, min_brightness=0.4, max_brightness=1.0,
                              ease_func=pytweening.easeInOutCubic)


def action_colorcycle():
    return ColorCycle(pixels, 5, ascending=False)


def main():
    pixels.brightness = 0.5
    # set_sequential(pixels, 0)
    pixels[:] = [COL_RED for i in range(len(pixels))]
    # set_random(pixels)
    time.sleep(2)
    pixels.show()

    # pixels[num_pixels // 2 + 1: num_pixels] = COL_RED

    # from found_example_code.adafruit_learn_neopixel.adafruit_neopixel_annotated import color_chase
    # while True:
    #     color_chase(pixels, COL_RED, 0.01)
    #     color_chase(pixels, COL_GREEN, 0.01)
    #     color_chase(pixels, COL_BLUE, 0.01)

    print('creating actions to run')
    actions = {
        action_bright_pingpong(),
        # action_colorcycle(),

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

    # just here to prototype stuff instead of main quickly
    while True:
        pass
finally:
    pixels.fill(COL_BLACK)
    pixels.show()
    print('Exiting...')
