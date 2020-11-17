import pytweening
import board
from neopixel import NeoPixel
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
    return BrightnessPingPong(pixels, half_cycle_time=half_cycle_time, min_brightness=0.0, max_brightness=0.8,
                              ease_func=pytweening.easeInOutCubic, on_halfcycle_finished=callback)


def rand_deep_color(min_sat: float = 0.8, max_lum: float = 0.6):
    sat = random.uniform(min_sat, 1)
    hue = random.uniform(0, max_lum)
    lum = random.uniform(0, 1)
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



def main():
    pixels.brightness = 0.6
    # colorREPL()
    # set_sequential(pixels, 0)
    pixels[:] = [COL_RED for i in range(len(pixels))]
    # set_random(pixels)
    time.sleep(2)
    pixels.show()

    # print(random.__file__)
    def darker_rand_func():
        result = tuple((int(random.uniform(0, 120)) for i in range(3)))
        return result

    # pixels[num_pixels // 2 + 1: num_pixels] = COL_RED

    # from found_example_code.adafruit_learn_neopixel.adafruit_neopixel_annotated import color_chase
    # while True:
    #     color_chase(pixels, COL_RED, 0.01)
    #     color_chase(pixels, COL_GREEN, 0.01)
    #     color_chase(pixels, COL_BLUE, 0.01)

    def on_brightness_halfcycle(i: int):
        print(i)
        if i % 2 == 0:
            set_random(pixels, rand_func_max_colors(5, rand_deep_color))
            # set_random(pixels, rand_func_max_colors(5))

    print('creating actions to run')
    actions = {
        action_bright_pingpong(5, on_brightness_halfcycle),
        # action_colorcycle(5),

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
