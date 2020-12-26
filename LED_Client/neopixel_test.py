import pytweening
import board
from neopixel import NeoPixel
import time

from random import Random
from typing import *
from Utils.color_util import *
from led_actions.LambdaAction import LambdaAction
from led_actions.LedAction import LedAction
from led_actions.BrightnessPingPongAction import BrightnessPingPong
from led_actions.ColorCycleAction import ColorCycle
from led_actions.BulgeLedAction import Bulge
from led_actions.SetRangesAction import SetRangesAction
from led_actions.NeoPixelWrappers import NeoPixelRange

random = Random()


class Actions_Basic:
    @classmethod
    def autoshow(cls, pixels, value: bool):
        pixels.auto_write = value
        if value:
            pixels.show()

    @classmethod
    def set_sequential(cls, pixels: NeoPixel, start_hue: float = 0, end_hue: float = 1):
        print('set sequential (start: {} -> end: {})'.format(start_hue, end_hue))
        num_pixels = len(pixels)
        for i in range(num_pixels):
            t = (i / num_pixels)
            hue = start_hue + t * (end_hue - start_hue)
            pixels[i] = get_rgb_bytes(hue, light=pixels.brightness)

    @classmethod
    def set_split(cls, pixels: NeoPixel, offset: float = 0.0):
        print('set split (offset: {})'.format(offset))
        num_pixels = len(pixels)
        half = num_pixels // 2

        halfLights = [get_rgb_bytes(i / half) for i in range(half)]
        print(halfLights)
        print(len(halfLights), len(pixels))
        pixels[:half] = halfLights
        pixels[half:] = list(reversed(halfLights))

    @classmethod
    def set_random(cls, pixels: NeoPixel, rand_color_func: Callable[[], RGBBytesColor]):
        test = [rand_color_func() for i in range(len(pixels))]
        pixels[:] = test


class Actions_Breathe:

    @classmethod
    def breathe_rand(cls, pixels, fnRandCol: ColorGetter, rise_time: float):
        def on_brightness_halfcycle(i: int):
            print(i)
            if i % 2 == 0:
                Actions_Basic.set_random(pixels, rand_func_max_colors(4, rand_deep_color))
                # dont set min brightness to 0 since that messes up hue calculation for other funcs

        return BrightnessPingPong(pixels, half_cycle_time=4,
                                  min_brightness=0.0, max_brightness=0.45,
                                  ease_func=pytweening.easeInOutCubic,
                                  on_halfcycle_finished=on_brightness_halfcycle)
        # action_bright_pingpong(4, on_brightness_halfcycle)

    @classmethod
    def bright_pingpong_2(cls, pixels, half_cycle_time, callback=None):
        # dont set min brightness to 0 since that messes up hue calculation for other funcs
        return BrightnessPingPong(pixels, half_cycle_time=half_cycle_time, min_brightness=0.3, max_brightness=0.8,
                                  ease_func=pytweening.easeInOutCubic, on_halfcycle_finished=callback)


class Actions_ColorCycle:
    @classmethod
    def colorcylce(cls, pixels, iter_time: float):
        return ColorCycle(pixels, iter_time, ascending=False)

    @classmethod
    # fills the strip one by one. Could be nice if async so I can send waves on top of each other
    def color_chase(cls, pixels, color, pix_wait, cycle_wait):
        for i in range(len(pixels)):
            pixels[i] = color
            time.sleep(pix_wait)
            pixels.show()
        time.sleep(cycle_wait)


def Actions_Interactive_ColorREPL(pixels):
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


def rand_func_max_colors(size: int, inner_rand_color: Callable[[], RGBBytesColor] = rand_color) -> Callable[
    [], RGBBytesColor]:
    if size <= 0:
        raise ValueError
        raise ValueError
    set_ = [inner_rand_color() for i in range(size)]
    return lambda: rand_colors_from_list(set_)


def rand_colors_from_list(color_set: Sequence[RGBBytesColor]) -> RGBBytesColor:
    return random.choice(color_set)


def rand_deep_color(min_sat: float = 0.9, lum=0.75):
    sat = random.uniform(min_sat, 1)
    hue = random.uniform(0, 1)
    return get_rgb_bytes(hue, sat, lum)


def event_loop(pixels, actions: Set[LedAction]):
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


def init():
    ADDRESSABLE_LEDS = 30  # (30/m * 5m) / 3 [Addr is Groups of 3]
    print('Setting up neopixel + clearing lights')

    pixels = NeoPixel(board.D18, ADDRESSABLE_LEDS, brightness=1, auto_write=False, pixel_order="BRG")
    pixels.fill(COL_BLACK)
    pixels.show()

    return pixels


def main(pixels: NeoPixel):
    golden_yellow = html_to_rgb_bytes("#ff9900")
    red = (255, 0, 00)
    START_COL = red
    # Actions_Basic.autoshow(pixels, True)

    pixels.brightness = 0.6
    pixels.fill(START_COL)

    prange = NeoPixelRange(pixels, slice(3, len(pixels), 4))

    prange.set_colors(COL_BLACK)
    prange.show()

    print('creating actions to run')

    def toggle_lights(iters):
        print('toggle. 4ths enabled: {}, between enabled: {}'.format(turn_off_4ths.enabled,
                                                                     turn_off_between_4ths.enabled))
        turn_off_4ths.toggle_enabled()
        turn_off_between_4ths.toggle_enabled()

    fourths = range(0, len(pixels), 4)
    between_4ths_ranges = tuple(map(lambda i: NeoPixelRange(pixels, slice(i, i + 3)), fourths))

    breathe_action = Actions_Breathe.bright_pingpong_2(pixels, 4, toggle_lights)

    set_colors_lambda = lambda: Actions_Basic.set_sequential(pixels, 0, 0.1)
    set_colors = LambdaAction.start_and_update(set_colors_lambda)

    turn_off_4ths = SetRangesAction(NeoPixelRange(pixels, slice(3, None, 4)), COL_BLACK)
    turn_off_between_4ths = SetRangesAction(between_4ths_ranges, COL_BLACK)

    turn_off_between_4ths.enabled = False

    actions = {
        set_colors,
        breathe_action,
        turn_off_4ths,
        turn_off_between_4ths,
        # Actions_Breathe.breathe_rand(pixels, rand_deep_color, 4),
        # Actions_ColorCycle.colorcylce(pixels, 5),
        # Bulge(3, pixels, START_COL, rand_deep_color, 0.0055), # TODO: Easing
    }

    event_loop(pixels, actions)


##########
#############
#########

new_pixels = init()
try:
    main(new_pixels)
    while True:
        pass  # just here to prototype stuff instead of main quickly
finally:
    new_pixels.fill(COL_BLACK)
    new_pixels.show()
    print('Exiting...')
