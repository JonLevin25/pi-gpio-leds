from math import sin, pi
from typing import Union, Callable, Mapping

import pytweening
from neopixel import NeoPixel

from LED_Server.glove_functions import GLOVE_HACKS
from LED_Server.glove_functions.Finger import FlashFinger
from Utils.color_util import *
from Utils.math_util import *
from led_actions.base.LedAction import LedAction
from led_actions.experimental.NeoPixelWrappers import NeoPixelRange

HAND_LEFT = 0
HAND_RIGHT = 1

FINGER_IDX = 0
FINGER_MID = 1
FINGER_RING = 2
FINGER_PINKY = 3
# FINGER_THUMB = 4

def left_idx_finger_action(pixels: NeoPixel, name: str):
    return fastFlashLtR(pixels, COL_BLUE, name)

def left_mid_finger_action(pixels, name: str):
    return fastFlashLtR(pixels, COL_RED, name)


finger_dict = {
    (HAND_LEFT, FINGER_IDX): FlashFinger("LEFT INDEX", HAND_LEFT, FINGER_IDX, left_idx_finger_action, holdAction= left_idx_finger_action),
    (HAND_LEFT, FINGER_MID): FlashFinger("LEFT MIDDLE", HAND_LEFT, FINGER_MID, left_mid_finger_action, holdAction= left_mid_finger_action),
    (HAND_LEFT, FINGER_RING): None,
    (HAND_LEFT, FINGER_PINKY): None,

    (HAND_RIGHT, FINGER_IDX): None,
    (HAND_RIGHT, FINGER_MID): None,
    (HAND_RIGHT, FINGER_RING): None,
    (HAND_RIGHT, FINGER_PINKY): None,
}

def on_glove_finger_down(pixels: NeoPixel, hand: int, finger: int) -> Union[LedAction, None]:
    finger = finger_dict[(hand, finger)]
    return finger.on_finger_down(pixels)

def on_glove_finger_press(pixels: NeoPixel, hand: int, finger: int):
    finger = finger_dict[(hand, finger)]
    return finger.on_finger_press(pixels)

def on_glove_finger_up(pixels: NeoPixel, hand: int, finger: int):
    finger = finger_dict[(hand, finger)]
    return finger.on_finger_up(pixels)


def fastFlashLtR(pixels, color: RGBBytesColor, name: str="GENERIC") -> 'GloveFingerFlashAction':
    return GloveFingerFlashAction(pixels,
                                  0, 30,
                                  delta_led_lightup=GLOVE_HACKS.FAST_LED_DELTA, anim_time=GLOVE_HACKS.FAST_LED_ANIM_TIME,
                                  target_col=color,
                                  name=name)

def fastFlashRtL(pixels, color: RGBBytesColor, name: str="GENERIC") -> 'GloveFingerFlashAction':
    return GloveFingerFlashAction(pixels,
                                  30, 0,
                                  delta_led_lightup=GLOVE_HACKS.FAST_LED_DELTA, anim_time=GLOVE_HACKS.FAST_LED_ANIM_TIME,
                                  target_col=color,
                                  name=name)



class GloveFingerFlashAction(LedAction):
    def __init__(self, pixels: Union[NeoPixel],
                 led_start_idx: int,
                 led_stop_idx: int,
                 delta_led_lightup: float,
                 anim_time: float,
                 target_col: RGBBytesColor, # TODO: support list of colors>?
                 ascending = True,
                 name: str = "GENERIC"):
        super().__init__(pixels=pixels, iteration_time=1)
        self.ascending = ascending
        self.led_start_idx = led_start_idx
        self.led_stop_idx = led_stop_idx
        self.delta_led_lightup = delta_led_lightup
        self.anim_time = anim_time
        self.target_col = target_col
        self.pixels = pixels
        self.name = name

        pixLen = led_stop_idx - led_start_idx
        last_led_start_time = pixLen * delta_led_lightup
        self.destroy_t_offset = last_led_start_time + self.anim_time

    def _get_led_col(self, curr_t: float, i: int) -> RGBBytesColor:
        cur_pix_col = self.pixels[i]

        anim_start = self.start_time + i * self.delta_led_lightup
        if curr_t < anim_start: return cur_pix_col # dont affect until start

        anim_end = anim_start + self.anim_time

        # if curr_t > anim_end: return cur_pix_col
        i_t = inverse_lerp(curr_t, anim_start, anim_end)
        if i_t >\
                2: return cur_pix_col # completed fade in + out already

        adjusted_t = sin(i_t * pi) * 0.5 + 0.5

        return color_lerp_rgb(adjusted_t, cur_pix_col, self.target_col)

    def _update(self, t: float, dt: float):
        if t > self.start_time + self.destroy_t_offset:
            print(f"Destroying Finger action! ({self.name})")
            self.destroy()

        for i in range(self.led_start_idx, self.led_stop_idx):
            col = self._get_led_col(t, i)
            self.pixels[i] = col
