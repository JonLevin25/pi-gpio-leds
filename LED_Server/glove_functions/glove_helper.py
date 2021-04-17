from typing import Union, Callable

import pytweening
from neopixel import NeoPixel

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

# TODO: Return LedAction
def index_finger(pixels):
    print("INDEX FINGER!")
    pixRange = NeoPixelRange(pixels, slice(0, 4))
    return GloveFingerFlashAction(pixRange,
                                  delta_led_lightup=0.2, anim_time=0.4,
                                  target_col= COL_GREEN,
                                  name="INDEX FINGER")

def middle_finger(pixels):
    print('MIDDLE FINGER!')
    pixRange = NeoPixelRange(pixels, slice(0, 4))
    return GloveFingerFlashAction(pixRange,
                                  delta_led_lightup=0.2, anim_time=0.4,
                                  target_col=COL_RED,
                                  name="MIDDLE FINGER")

fn_dict = {
    (HAND_LEFT, FINGER_IDX): index_finger,
    (HAND_LEFT, FINGER_MID): middle_finger,
    (HAND_LEFT, FINGER_RING): None,
    (HAND_LEFT, FINGER_PINKY): None,

    (HAND_RIGHT, FINGER_IDX): None,
    (HAND_RIGHT, FINGER_MID): None,
    (HAND_RIGHT, FINGER_RING): None,
    (HAND_RIGHT, FINGER_PINKY): None,
}

def glove_request_handler(pixels: NeoPixel, hand: int, finger: int) -> Union[LedAction, None]:
    return fn_dict[(hand, finger)](pixels)



class GloveFingerFlashAction(LedAction):
    def __init__(self, pixels: Union[NeoPixel, NeoPixelRange], delta_led_lightup: float, anim_time: float,
                 target_col: RGBBytesColor, # TODO: support list of colors>?
                 ascending = True,
                 name: str = "GENERIC"):
        super().__init__(pixels=pixels, iteration_time=1)
        self.ascending = ascending
        self.delta_led_lightup = delta_led_lightup
        self.anim_time = anim_time
        self.target_col = target_col
        self.pixels = pixels
        self.name = name

        last_led_start_time = len(pixels) * delta_led_lightup
        self.destroy_time = last_led_start_time + self.anim_time

    def _get_led_col(self, curr_t: float, i: int) -> RGBBytesColor:
        anim_start = i * self.delta_led_lightup
        anim_end = anim_start + self.anim_time
        i_t = inverse_lerp(curr_t, anim_start, anim_end)

        return color_lerp_rgb(i_t, self.pixels[i], self.target_col)

    def _update(self, t: float, dt: float):
        if t > self.destroy_time:
            print(f"Destroying Finger action! ({self.name})")
            self.destroy()

        for i in range(len(self.pixels)):
            col = self._get_led_col(t, i)
            self.pixels[i] = col
