from typing import Iterable, Callable

import neopixel

from Utils.color_util import RGBBytesColor
from Utils.misc_util import FnVoid
from led_actions.base.ActionQueue import ActionQueue
from led_actions.base.LambdaAction import LambdaAction
from led_actions.base.LedAction import LedAction
from led_actions.experimental.NeoPixelWrappers import NeoPixelRange
from led_actions.actions.BrightnessPingPongAction import BrightnessPingPong
from led_actions.actions.SetRangesAction import SetRangesAction


def FillGapsAction(pixels: neopixel.NeoPixel, color_setter: FnVoid,
                   fill_length: int, gap_length: int,
                   half_cycle_time: float,
                   min_brightness: float = 0.2, max_brightness: float = 1.0,
                   on_halfcycle: Callable[[int], None] = None
                   ) -> LedAction:
    """
    A composite action effect that:
     1) defines a color range thats shown
     2) Turns off <gap_length> pixels after every <fill_length> pixels that are on.
        (<fill> on - <gap> off - <fill> on - <gap> off ...)
     3) runs a "brightness breathe" action.
     4) on minimum brightness, toggles <gap> / <fill> leds so that those that were off are now on, and vise-versa.

    """

    def on_brightness_halfcycle(iters: int):
        if iters % 2 == 0:
            toggle_lights()
        if on_halfcycle:
            on_halfcycle(iters)

    def toggle_lights():
        turn_off_gaps.toggle_enabled()
        turn_off_between_gaps.toggle_enabled()

    def get_pixel_ranges(totallen: int, offset: int, itemlen: int, gaplen: int) -> Iterable[NeoPixelRange]:
        def get_slice(start_idx):
            return slice(start_idx, min(start_idx + itemlen, totallen), 1)

        start_indices = range(offset, totallen, itemlen + gaplen)
        return list(NeoPixelRange(pixels, get_slice(i)) for i in start_indices)

    COL_BLACK: RGBBytesColor = (0, 0, 0)

    pixlen = len(pixels)
    fills_ranges = get_pixel_ranges(pixlen, offset=0, itemlen=fill_length, gaplen=gap_length)
    gaps_ranges = get_pixel_ranges(pixlen, offset=fill_length, itemlen=gap_length, gaplen=fill_length)

    breathe_action = BrightnessPingPong(pixels, half_cycle_time,
                                        min_brightness, max_brightness,
                                        on_halfcycle_finished=on_brightness_halfcycle)

    set_colors = LambdaAction.from_function(color_setter)
    turn_off_gaps = SetRangesAction(gaps_ranges, COL_BLACK)
    turn_off_between_gaps = SetRangesAction(fills_ranges, COL_BLACK)

    turn_off_between_gaps.enabled = False

    return ActionQueue([
        set_colors,
        breathe_action,
        turn_off_gaps,
        turn_off_between_gaps,
    ])
