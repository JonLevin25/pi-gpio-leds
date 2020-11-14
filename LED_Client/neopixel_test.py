import pytweening
import board
import neopixel
import time

from typing import *
from Utils.color_util import *
from Utils.math_util import *

ADDRESSABLE_LEDS = 30  # (30/m * 5m) / 3 [Addr is Groups of 3]

pixels = neopixel.NeoPixel(board.D18, ADDRESSABLE_LEDS, brightness=1, auto_write=False)

pixels.fill(COL_BLACK)
pixels.show()

T = TypeVar('T')


# TODO: Convert to generic "Tween" / "LedAction" class
class TempBase(Generic[T]):
    def __init__(self, pixels: List[neopixel.NeoPixel], iteration_time: float):
        if iteration_time <= 0:
            raise ValueError("Iteration time muse be positive!")

        self.pixels = pixels
        self.iteration_time = iteration_time
        self.norm_t_offset = 0

    def tick(self, curr_time: float):
        dt = curr_time - self.prev_tick
        self._update(curr_time, dt)
        self.prev_tick = curr_time

    def run(self, curr_time: float):
        self.start_time = curr_time
        self.prev_tick = curr_time
        self._start(curr_time)

    @property
    def norm_t_offset(self) -> float:
        return self._norm_t_offset

    @norm_t_offset.setter
    def norm_t_offset(self, value: float):
        self._norm_t_offset = value

    def get_norm_t(self, t: float):
        norm_t_unclamped = (t - self.start_time) / self.iteration_time + self.norm_t_offset
        return norm_t_unclamped % 1

    def get_norm_dt(self, dt: float):
        return dt / self.iteration_time

    def _start(self, start_time: float):
        pass

    def _update(self, t: float, dt: float):
        """
        t: the time since start
        dt: the time since last update
        """
        pass


class TempBasePingPong(TempBase):
    def get_norm_t_pingpong(self, t: float):
        norm_t_unclamped = (t - self.start_time) / self.iteration_time + self.norm_t_offset
        complete_iters = int(norm_t_unclamped)
        curr_ascending = self.start_ascending ^ complete_iters % 2  # true if currently ascending

        naive_norm_t = norm_t_unclamped % 1
        return naive_norm_t if curr_ascending else 1 - naive_norm_t


class BrightnessPingPong(TempBasePingPong):
    def __init__(self, pixels, half_cycle_time: float, min_brightness: float, max_brightness: float,
                 start_ascending=True,
                 ease_func: Callable[[float], float] = pytweening.linear):
        MIN_ALLOWED_BRIGHTNESS = 0.0
        MAX_ALLOWED_BRIGHTNESS = 0.99  # to avoid getting stuck

        super().__init__(pixels=pixels, iteration_time=half_cycle_time)
        self.min_brightness = max(min_brightness, MIN_ALLOWED_BRIGHTNESS)
        self.max_brightness = min(max_brightness, MAX_ALLOWED_BRIGHTNESS)
        self.start_ascending = start_ascending
        self.ease_func = ease_func

    def clamp_brightness(self, b: float) -> float:
        return max(min(b, self.max_brightness), self.min_brightness)

    def get_brightness(self) -> float:
        return self.pixels.brightness

    def set_brightness(self, val: float):
        self.pixels.brightness = val

    def get_b(self, norm_t: float) -> float:
        eased_t = self.ease_func(norm_t)
        b = lerp(eased_t, self.min_brightness, self.max_brightness)
        return self.clamp_brightness(b)

    def _start(self, t):
        self.norm_t_offset = inverse_lerp(self.get_brightness(), self.min_brightness, self.max_brightness)

    def _update(self, t: float, dt: float):
        norm_t = self.get_norm_t_pingpong(t)
        new_b = self.get_b(norm_t)
        # print('Asc: {}, t: {}, curr_b: {}, new_b: {}, clamped: {}. Range[{}, {}]'.format(self.ascending, t, curr_b, new_b, clamped_new_b, self.min_brightness, self.max_brightness))
        print('norm_t: {:.3f}, new_b: {:.3f}'.format(norm_t, new_b))
        pixels.brightness = new_b


# TODO: Finish this
# work with deltas so it reacts to outside changes
class ColorCycle(TempBase):
    def __init__(self, pixels: List[neopixel.NeoPixel], cycle_time: float, start_ascending=True,
                 ease_func: Callable[[float], float] = pytweening.linear):
        super().__init__(pixels=pixels, iteration_time=cycle_time)
        self.start_ascending = start_ascending
        self.ease_func = ease_func
        self.pixels = pixels

    @property
    def colors(self) -> Iterable[Iterable[float]]:
        self.pixels[:]

    @colors.setter
    def colors(self, value: Iterable[Iterable[float]]):
        self.pixels[:len(value)] = value

    def get_next(self, pixel, dt: float) -> float:
        norm_dt = self.get_norm_dt(dt)
        (old_h, s, v) = get_hsv(pixel)
        naive_new_hue = (old_h + norm_dt) % 1
        new_hue = self.ease_func(naive_new_hue)

        rgb_bytes = get_rgb_bytes(new_hue, s, v)
        return rgb_bytes

    def _start(self, t: float):
        pass

    def _update(self, t: float, dt: float):
        for i in range(len(self.pixels)):
            p = self.pixels[i]
            new_p = self.get_next(p, dt)
            self.pixels[i] = new_p


def test_color_cycle():
    while True:
        for i in range(len(pixels)):
            p = pixels[i]
            new_p = add_hue(p, 0.002)
            pixels[i] = new_p
        pixels.show()

        time.sleep(0.0000000001)


# convenience actions, just so its easier to comment lines out in actions set
def action_bright_pingpong():
    return BrightnessPingPong(pixels, half_cycle_time=2.5, min_brightness=0.0, max_brightness=1.0,
                       ease_func=pytweening.easeInOutCubic),


def action_colorcycle():
    return ColorCycle(pixels, 10)


def main():
    test = [rand_color() for i in range(len(pixels))]
    pixels[:] = test
    # pixels.brightness = 0

    print('creating actions to run')
    actions = {
        # action_bright_pingpong(),
        action_colorcycle(),

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
finally:
    print('creating actions to run')
    pixels.fill(COL_BLACK)
    pixels.show()
    print('Exiting...')

