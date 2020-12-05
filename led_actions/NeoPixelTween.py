from typing import Union, Tuple, List, Iterable, Callable, TypeVar, Generic

from neopixel import NeoPixel
from led_actions.NeoPixelWrappers import NeoPixelRange
from pytweening import linear

Color = Union[Tuple[int], List[int]]
T = TypeVar('T')
TGetter = Callable[[], T]
TSetter = Callable[[T], None]
TOperation = Callable[[T, T], T]
TScale = Callable[[T, float], T]
TEasing = Callable[[float], float]


# impl w/ delta
def to_colors_start(pixelRange: NeoPixelRange, toColors: Union[Color, Iterable[Color]], duration: float):
    pass


def to_colors_update(pixelRange: NeoPixelRange, toColors: Union[Color, Iterable[Color]]):
    pass


# expects T to impl +(T,T); -(T,T); *(T,float)
class TweenTo(Generic[T]):
    def __init__(self,
                 getter: TGetter,
                 setter: TSetter,
                 target_value: T,
                 duration: float,
                 unit_value: T,
                 easing: TEasing = linear,
                 add_func: TOperation = lambda t1, t2: t1 + t2,
                 sub_func: TOperation = lambda t1, t2: t1 - t2,
                 scale_func: TScale = lambda t1, k: t1 * k,
                 ):
        # separate errors for stacktrace
        if duration <= 0: raise ValueError
        if not getter: raise ValueError
        if not setter: raise ValueError
        if not target_value: raise ValueError

        # generic math stuff
        self.target_unit = unit_value
        self.add_func = add_func
        self.sub_func = sub_func
        self.scale_func = scale_func

        self.getter = getter
        self.setter = setter
        self.target = target_value
        self.duration = duration
        self.prev_t = 0

        self.init_value = getter()

    def update(self, t):
        # The amount of T that should change in this frame
        self.init_value

        curr_val = self.getter()
        next_val = self.add_func(curr_val, delta_val)
        self.setter(next_val)

        self.prev_t = t



class NeoPixelTween:
    def __init__(self, pixels: Union[NeoPixelRange, NeoPixel], duration: float, easing=linear):
        if duration <= 0:
            raise ValueError("Iteration time muse be positive!")

        self.pixelRange = pixels if isinstance(pixels, NeoPixelRange) else NeoPixelRange(pixels)
        self.duration = duration
        self.easing = easing

    def start(self, curr_time: float):
        self.start_time = curr_time
        self.prev_tick = curr_time
        self._start(curr_time)

    def update(self, curr_time: float):
        dt = curr_time - self.prev_tick
        self._update(curr_time, dt)
        self.prev_tick = curr_time

    def _start(self, start_time: float):
        pass

    def _update(self, dt: float):
        """
        t: the time since start
        dt: the time since last update
        """
        pass
