import neopixel
import pytweening

from Utils.color_util import *
from Utils.math_util import *
from led_actions.base.LedAction import LedAction
from led_actions.experimental.NeoPixelWrappers import NeoPixelRange
from random import Random

random = Random()



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
                 base_color: RGBBytesColor,
                 rand_func: Callable[[], RGBBytesColor],
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


    def _tweenToThenTo(self, start_t: float, pixIdx: int, target1: RGBBytesColor, target2: RGBBytesColor, totalDuration: float):
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
