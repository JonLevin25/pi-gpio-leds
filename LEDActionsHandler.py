import time
from random import Random
from typing import *

import pytweening
from neopixel import NeoPixel

from Utils.ActionsRouter import ActionsRouter
from Utils.PixelsActionsRouter import PixelsActionsRouter
from Utils.color_util import *
from led_actions.Basic.NeoPixelWrappers import NeoPixelRange
from led_actions.BrightnessPingPongAction import BrightnessPingPong
from led_actions.ColorCycleAction import ColorCycle

random = Random()

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
    set_ = [inner_rand_color() for i in range(size)]
    return lambda: rand_colors_from_list(set_)


def rand_colors_from_list(color_set: Sequence[RGBBytesColor]) -> RGBBytesColor:
    return random.choice(color_set)


def rand_deep_color(min_sat: float = 0.9, lum=0.75):
    sat = random.uniform(min_sat, 1)
    hue = random.uniform(0, 1)
    return get_rgb_bytes(hue, sat, lum)

class Actions_Test:
    @classmethod
    def test_rgb(cls, pixels, pause: float = 2):
        for col in ((255,0,0), (0, 255, 0), (0, 0, 255)):
            pixels.fill(col)
            pixels.show()
            time.sleep(pause)


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

    @classmethod
    def set_range(cls, pixels: NeoPixel, range_slice: slice, col: RGBBytesColor, clear_others: bool = False):
        if clear_others:
            pixels.fill(COL_BLACK)
        pix_range = NeoPixelRange(pixels, range_slice)
        pix_range.set_colors(col)


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

def is_float(string):
    try:
        int(string)
    except:
        return False
    return True

def is_int(string):
    try:
        int(string)
    except:
        return False
    return True

def parse_int(string: str):
    try:
        return int(string)
    except:
        print(f'Could not parse "{string}" to int!')

def parse_num(string: str):
    try:
        return float(string)
    except:
        return int(string)

def set_brightness(pixels: NeoPixel, value: float):
    pixels.brightness = value

def test_fill_rand(pixels: NeoPixel, max_colors: int):
    Actions_Basic.set_random(pixels, rand_func_max_colors(max_colors, rand_deep_color))