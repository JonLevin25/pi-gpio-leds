from typing import *

import neopixel
import pytweening

from Utils.color_util import *
from Utils.math_util import *
from led_actions.LedAction import LedAction
from led_actions.NeoPixelWrappers import NeoPixelRange
from random import Random

Color = Union[Tuple[int, int, int], List[int]]

random = Random()


def mapTo(x: float, srcRange: Tuple[float, float], destRange: Tuple[float, float]):
    srcDelta = srcRange[1] - srcRange[0]
    t = (x - srcRange[0]) / srcDelta

    destDelta = destRange[1] - destRange[0]
    return destRange[0] + (t * destDelta)


def color_lerp_hsv(t: float, from_col: Color, to_col: Color):
    f_h, f_s, f_l = get_hsv(from_col)
    t_h, t_s, t_l = get_hsv(to_col)

    posdelta = t_h - f_h
    negdelta = -(256-t_h) - f_h
    if abs(negdelta) < abs(posdelta):
        t_h -= 256

    h = mapTo(t, (0, 1), (f_h, t_h))
    s = mapTo(t, (0, 1), (f_s, t_s))
    l = mapTo(t, (0, 1), (f_l, t_l))

    if (h < 0):
        h += 256
    return get_rgb_bytes(h, s, l)


def color_lerp_rgb(t: float, from_col: Color, to_col: Color):
    f_r, f_g, f_b = from_col
    t_r, t_g, t_b = to_col

    raw_r = lerpInt(t, f_r, t_r)
    raw_g = lerpInt(t, f_g, t_g)
    raw_b = lerpInt(t, f_b, t_b)

    r = clampInt(raw_r, 0, 255)
    g = clampInt(raw_g, 0, 255)
    b = clampInt(raw_b, 0, 255)

    return (r, g, b)


class PrintAvg:
    def __init__(self, samples, every):
        self.rolling = []
        self.samples = samples
        self.every = every
        self.counter = 0

    def tick(self, value):
        self.rolling.append(value)
        self.counter += 1

        if len(self.rolling) <= self.samples:
            return

        self.rolling.pop(0)

        if self.counter % self.every == 0:
            print(f'avg: {sum(self.rolling) / self.samples}')


class Bulge(LedAction):
    def __init__(self,
                 bulge_time: float,
                 pixels: Union[neopixel.NeoPixel, NeoPixelRange],
                 base_color: Color,
                 rand_func: Callable[[], Color],
                 bulge_chance: float,
                 ):

        super().__init__(pixels=pixels, iteration_time=bulge_time)

        self.bulge_time = bulge_time
        self.bulge_chance = bulge_chance
        self.pixels = pixels
        self.base_color = base_color
        self.rand_func = rand_func
        self._running_tweens = []
        self.printavg = PrintAvg(30, 100)

    def _start(self, t: float):
        pass

    def _update(self, t: float, dt: float):

        # TODO: better random algo?
        chance = self.bulge_chance
        rand = random.random()

        should_bulge = rand < chance
        self.printavg.tick(chance)
        if should_bulge:
            led_to_bulge = self.get_rand_led_idx()
            if led_to_bulge != -1:
                target_color = self.rand_func()

                print('animate ' + str(led_to_bulge))
                # "bulge" to a certain color then back to base
                new_tween = self._tweenToThenTo(t, led_to_bulge, target_color, self.base_color, self.bulge_time)
                self._running_tweens.append((led_to_bulge, new_tween))

        finished = []
        for i in range(len(self._running_tweens)):
            (led_i, tween) = self._running_tweens[i]
            done = tween(t)
            if done:
                finished.append(i)

        finished.reverse()
        for i in finished:
            print('Removing ' + str(self._running_tweens[i][0]))

            del self._running_tweens[i]
        # print('animating: {}'.format(tuple(map(lambda x: x[0], self._running_tweens))))


    def get_rand_led_idx(self, tries: int = 0):
        if tries > 4:
            return -1

        def get():
            if isinstance(self.pixels, slice):
                s = self.pixels
                return random.choice(range(s.start, s.stop, s.step))
            return random.choice(range(len(self.pixels)))
        i = get()
        curr_animating_leds = map(lambda tup: tup[0], self._running_tweens)
        if i in curr_animating_leds:
            return self.get_rand_led_idx(tries+1)
        return i


    def _tweenToThenTo(self, start_t: float, pixIdx: int, target1: Color, target2: Color, totalDuration: float):
        startCol = self.pixels[pixIdx]
        end_t = start_t + totalDuration
        switch_t = start_t + 0.5 * totalDuration

        def tween(progress: float, from_col: RGBBytesColor, to_col: RGBBytesColor, ease: Callable[[float], float] = pytweening.linear):
            progress = ease(progress)
            return color_lerp_rgb(progress, from_col, to_col)

        def update_tween(t: float):
            is_done = t > end_t
            if is_done:
                return True
            is_first_tween = t < switch_t
            if is_first_tween:
                progress = (t - start_t) / (switch_t - start_t)
                col = tween(progress, startCol, target1)
                self.pixels[pixIdx] = col
            else:
                progress = (t - switch_t) / (end_t - switch_t)
                col = tween(progress, target1, target2)
                self.pixels[pixIdx] = col
            return False

        return update_tween
