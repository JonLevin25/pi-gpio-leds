import pytweening
import board
from neopixel import NeoPixel
from led_actions.NeoPixelRange import NeoPixelRange
import time

from random import Random
from typing import *
from Utils.color_util import *
from Utils.math_util import *
from led_actions.BrightnessPingPongAction import BrightnessPingPong
from led_actions.ColorCycleAction import ColorCycle

ADDRESSABLE_LEDS = 30  # (30/m * 5m) / 3 [Addr is Groups of 3]

print('Setting up neopixel + clearing lights')
pixels = NeoPixel(board.D18, ADDRESSABLE_LEDS, brightness=1, auto_write=False)
pixels.fill(COL_BLACK)
pixels.show()

random = Random()


def set_sequential(pixels: NeoPixel, offset: float = 0.0):
    num_pixels = len(pixels)
    for i in range(num_pixels):
        hue = (i / num_pixels) + offset
        pixels[i] = get_rgb_bytes(hue, light=pixels.brightness)


def set_random(pixels: NeoPixel, rand_color_func: Callable[[], Tuple[int]]):
    test = [rand_color_func() for i in range(len(pixels))]
    pixels[:] = test


def rand_func_max_colors(size: int, inner_rand_color: Callable[[], Tuple[int]] = rand_color) -> Callable[
    [], Tuple[int]]:
    if size <= 0:
        raise ValueError
        raise ValueError
    set_ = [inner_rand_color() for i in range(size)]
    return lambda: rand_colors_from_list(set_)


def rand_colors_from_list(color_set: Sequence[Tuple[int]]) -> Tuple[int]:
    return random.choice(color_set)


# convenience actions, just so its easier to comment lines out in actions set
def action_bright_pingpong(half_cycle_time, callback=None):
    # dont set min brighness to 0 since that messes up hue calculation for other funcs
    return BrightnessPingPong(pixels, half_cycle_time=half_cycle_time, min_brightness=0.0, max_brightness=0.45,
                              ease_func=pytweening.easeInOutCubic, on_halfcycle_finished=callback)

def action_bright_pingpong_2(half_cycle_time, callback=None):
    # dont set min brighness to 0 since that messes up hue calculation for other funcs
    return BrightnessPingPong(pixels, half_cycle_time=half_cycle_time, min_brightness=0.3, max_brightness=0.8,
                              ease_func=pytweening.easeInOutCubic, on_halfcycle_finished=callback)


def rand_deep_color(min_sat: float = 0.9, lum=0.75):
    sat = random.uniform(min_sat, 1)
    hue = random.uniform(0, 1)
    return get_rgb_bytes(hue, sat, lum)


def action_colorcycle(iter_time):
    return ColorCycle(pixels, iter_time, ascending=False)


def colorREPL():
    def parse_inp(user_input: str):
        def parse_col(col: str):
            try:
                stripped_col = col.strip()
                parsed = int(stripped_col)
                print('parsed {} -> {}'.format(col, parsed))
                return parsed if parsed in range(0, 256) else None
            except:
                return None

        split = user_input.split(' ')
        if len(split) != 3:
            return None

        result = tuple(parse_col(x) for x in split)
        return result if all(x is not None for x in result) else None

    print('Accepting input to fill pixels. Format: "R G B"')
    while True:
        inp = input('Pixels: ').strip()
        parsed_inp = parse_inp(inp)
        if parsed_inp is None:
            print('invalid! Format: "R G B" (range 0-255)')
            continue
        print('Parsed color: {}. Setting leds'.format(parsed_inp))
        pixels.fill(parsed_inp)
        pixels.show()


# fills the strip one by one. Could be nice if async so I can send waves on top of each other
def color_chase(pixels, color, pix_wait, cycle_wait):
    for i in range(len(pixels)):
        pixels[i] = color
        time.sleep(pix_wait)
        pixels.show()
    time.sleep(cycle_wait)


def main():
    pixels.brightness = 0.6
    # colorREPL()
    pixels[:] = [COL_RED for i in range(len(pixels))]
    # set_random(pixels)
    set_sequential(pixels, 0)
    time.sleep(2)
    pixels.show()

    # pixels[num_pixels // 2 + 1: num_pixels] = COL_RED

    def on_brightness_halfcycle(i: int):
        print(i)
        if i % 2 == 0:
            set_random(pixels, rand_func_max_colors(4, rand_deep_color))
            # set_random(pixels, rand_func_max_colors(5, rand_color))

    time.sleep(2)
    print('creating actions to run')
    actions = {
        # action_bright_pingpong(4, on_brightness_halfcycle),
        action_bright_pingpong_2(4),
        action_colorcycle(5),
    }
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
        time.sleep(0.001) # without this dt is sometimes too small


try:
    # main()

    print('START')
    r = NeoPixelRange(pixels)
    r.set_colors(COL_RED)
    r.show()
    print('END')

    # just here to prototype stuff instead of main quickly
    while True:
        pass
finally:
    pixels.fill(COL_BLACK)
    pixels.show()
    print('Exiting...')
