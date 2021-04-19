from math import sin, pi

from neopixel import NeoPixel

from LED_Server.glove_functions import GLOVE_HACKS
from LED_Server.glove_functions.Finger import FlashFinger
from LED_Server.glove_functions.GLOVE_HACKS import HAND_LEFT, HAND_RIGHT, FINGER_IDX, FINGER_MID, FINGER_RING, \
    FINGER_PINKY
from Utils.color_util import *
from Utils.math_util import *
from led_actions.base.LedAction import LedAction


def left_idx_finger_action(pixels: NeoPixel, name: str):
    return fastFlashLtR(pixels, GLOVE_HACKS.leftColor(), name)

def left_mid_finger_action(pixels, name: str):
    return fastFlashLtR(pixels, GLOVE_HACKS.leftColor(), name)

def right_idx_finger_action(pixels: NeoPixel, name: str):
    return fastFlashRtL(pixels, GLOVE_HACKS.rightColor(), name)

def right_mid_finger_action(pixels, name: str):
    return fastFlashRtL(pixels, GLOVE_HACKS.rightColor(), name)


finger_dict = {
    (HAND_LEFT, FINGER_IDX): FlashFinger("LEFT INDEX", HAND_LEFT, FINGER_IDX, GLOVE_HACKS.IDX_FINGER_COL,
                                         left_idx_finger_action, holdAction= left_idx_finger_action),
    (HAND_LEFT, FINGER_MID): FlashFinger("LEFT MIDDLE", HAND_LEFT, FINGER_MID, GLOVE_HACKS.MID_FINGER_COL,
                                         left_mid_finger_action, holdAction= left_mid_finger_action),
    (HAND_LEFT, FINGER_RING): None,
    (HAND_LEFT, FINGER_PINKY): None,

    (HAND_RIGHT, FINGER_IDX): FlashFinger("RIGHT INDEX", HAND_RIGHT, FINGER_IDX, GLOVE_HACKS.IDX_FINGER_COL,
                                          right_idx_finger_action, holdAction= right_idx_finger_action),
    (HAND_RIGHT, FINGER_MID): FlashFinger("RIGHT MIDDLE", HAND_RIGHT, FINGER_MID, GLOVE_HACKS.MID_FINGER_COL,
                                          right_mid_finger_action, holdAction= right_mid_finger_action),
    (HAND_RIGHT, FINGER_RING): None,
    (HAND_RIGHT, FINGER_PINKY): None,
}


def on_glove_finger_down(pixels: NeoPixel, hand: int, finger: int) -> Union[LedAction, None]:
    finger = finger_dict[(hand, finger)]
    return finger.on_finger_down(pixels)

#impl here, not in glove
# def on_glove_finger_hold(pixels: NeoPixel, hand: int, finger: int):
#     finger = finger_dict[(hand, finger)]
#     return finger.on_finger_hold(pixels)

def on_glove_finger_up(pixels: NeoPixel, hand: int, finger: int):
    finger = finger_dict[(hand, finger)]
    return finger.on_finger_up(pixels)


def on_glove_finger_tilt_down(pixels: NeoPixel, hand: int, finger: int):
    finger = finger_dict[(hand, finger)]
    return finger.on_tilt_down(pixels)

#impl here, not in glove
# def on_glove_finger_tilt_hold(pixels: NeoPixel, hand: int, finger: int):
#     finger = finger_dict[(hand, finger)]
#     return finger.on_tilt_hold(pixels)

def on_glove_finger_tilt_up(pixels: NeoPixel, hand: int, finger: int):
    finger = finger_dict[(hand, finger)]
    return finger.on_tilt_up(pixels)


def two_thirds_idx(pixels):
    return int(len(pixels)* 0.6666)

def fastFlashLtR(pixels, color: RGBBytesColor, name: str="GENERIC") -> 'GloveFingerFlashAction':
    return GloveFingerFlashAction(pixels,
                                  range(0, two_thirds_idx(pixels)),
                                  delta_led_lightup=GLOVE_HACKS.FAST_LED_DELTA, anim_time=GLOVE_HACKS.FAST_LED_ANIM_TIME,
                                  color=color,
                                  name=name)

def fastFlashRtL(pixels, color: RGBBytesColor, name: str="GENERIC") -> 'GloveFingerFlashAction':
    return GloveFingerFlashAction(pixels,
                                  range(len(pixels)-1,   two_thirds_idx(pixels)-1, -1),
                                  delta_led_lightup=GLOVE_HACKS.FAST_LED_DELTA, anim_time=GLOVE_HACKS.FAST_LED_ANIM_TIME,
                                  color=color,
                                  name=name)

class GloveFingerFlashAction(LedAction):
    def __init__(self, pixels: Union[NeoPixel],
                 led_range: range,
                 delta_led_lightup: float,
                 anim_time: float,
                 color: RGBBytesColor,  # TODO: support list of colors>?
                 ascending = True,
                 name: str = "GENERIC"):
        super().__init__(pixels=pixels, iteration_time=1)
        self.ascending = ascending
        self.led_range = led_range
        self.delta_led_lightup = delta_led_lightup
        self.anim_time = anim_time
        self.color = color
        self.pixels = pixels
        self.name = name

        pixLen = len(led_range)
        last_led_start_time = pixLen * delta_led_lightup
        self.destroy_t_offset = last_led_start_time + self.anim_time

    def _get_led_col(self, curr_t: float, cur_pix_col: RGBBytesColor, i: int) -> RGBBytesColor:
        anim_start = self.start_time + i * self.delta_led_lightup
        if curr_t < anim_start: return cur_pix_col # dont affect until start

        anim_end = anim_start + self.anim_time
        i_t = inverse_lerp(curr_t, anim_start, anim_end)

        # if curr_t > anim_end: return cur_pix_col
        if i_t >= 2: return cur_pix_col # completed fade in + out already

        adjusted_t = sin(i_t * pi) * 0.5 + 0.5

        return color_lerp_rgb(adjusted_t, cur_pix_col, self.color)

    def _update(self, t: float, dt: float):
        if t > self.start_time + self.destroy_t_offset:
            print(f"Destroying Finger action! ({self.name})")
            self.destroy()

        for i, led_i in enumerate(self.led_range):
            cur_pix_col = self.pixels[led_i]
            # if led_i in (0, 1, 2, 3):
            #     self.pixels[28] = COL_RED
            # else:
            #     self.pixels[led_i] = self.pixels[led_i]
            col = self._get_led_col(t, cur_pix_col, i)
            self.pixels[led_i] = col
        pass