from typing import Iterable, Callable

import neopixel

from Utils.color_util import RGBBytesColor
from Utils.misc_util import FnVoid
from led_actions.Basic.ActionQueue import ActionQueue
from led_actions.Basic.LambdaAction import LambdaAction
from led_actions.Basic.LedAction import LedAction
from led_actions.Basic.NeoPixelWrappers import NeoPixelRange
from led_actions.BrightnessPingPongAction import BrightnessPingPong
from led_actions.SetRangesAction import SetRangesAction


def FillGapsAction(pixels: neopixel.NeoPixel, color_setter: FnVoid,
                   fill_length: int, gap_length: int,
                   half_cycle_time: float,
                   min_brightness: float = 0.2, max_brightness: float = 1.0,
                   on_halfcycle: Callable[[int], None] = None
                   ) -> LedAction:
    def on_brightness_halfcycle(iters: int):
        if iters % 2 == 0:
            toggle_lights()
        if on_halfcycle:
            on_halfcycle(iters)

    def toggle_lights():
        turn_off_gaps.toggle_enabled()
        turn_off_between_gaps.toggle_enabled()

    def get_slices(totallen: int, offset: int, itemlen: int, gaplen: int) -> Iterable[slice]:
        def get_slice(start_idx):
            return slice(start_idx, min(start_idx + fill_length, totallen))

        start_idxs = range(offset, totallen, itemlen + gaplen)
        return map(get_slice, start_idxs)

    def get_pixel_ranges(totallen: int, offset: int, itemlen: int, gaplen: int) -> Iterable[NeoPixelRange]:
        pxslices = get_slices(totallen, offset, itemlen, gaplen)
        return map(lambda pxslice: NeoPixelRange(pixels, pxslice), pxslices)

    COL_BLACK: RGBBytesColor = (0, 0, 0)

    pixlen = len(pixels)
    fills_ranges = get_pixel_ranges(pixlen, 0, itemlen=fill_length, gaplen=gap_length)
    gaps_ranges = get_pixel_ranges(pixlen, offset=fill_length, itemlen=gap_length, gaplen=fill_length)

    breathe_action = BrightnessPingPong(pixels, half_cycle_time,
                                        min_brightness, max_brightness,
                                        on_halfcycle_finished=on_brightness_halfcycle)

    set_colors = LambdaAction.create(color_setter)
    turn_off_gaps = SetRangesAction(gaps_ranges, COL_BLACK)
    turn_off_between_gaps = SetRangesAction(fills_ranges, COL_BLACK)

    turn_off_between_gaps.enabled = False

    return ActionQueue([
        set_colors,
        breathe_action,
        turn_off_gaps,
        turn_off_between_gaps,
    ])
