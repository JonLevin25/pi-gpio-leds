from operator import __getitem__

from neopixel import NeoPixel
import itertools
from typing import Union, Iterable, Sized, Iterator, List, Tuple

Color = Union[List[int], Tuple[int]]


def _is_multi_colors(value) -> bool:
    first = value[0]
    return type(first) != int


def _get_cycled_colors(value, length) -> List[Sized]:
    if not _is_multi_colors(value):
        return list(itertools.repeat(value, length))
    return list(itertools.islice(itertools.cycle(value), length))


class NeoPixelRange:
    def __init__(self, pixels: NeoPixel, pixel_range: Union[int, slice] = None):
        if not pixels:
            raise ValueError('No pixels given!')
        if pixel_range is None:
            pixel_range = slice(None, None)  # entire range
        if not isinstance(pixel_range, (int, slice)):
            raise ValueError('Pixel indices must be an int or a slice!')

        self.pixels = pixels
        self.pixelRange = pixel_range if isinstance(pixel_range, slice) else slice(0, pixel_range)

    def __len__(self):
        pix_len = len(self.pixels)
        return len(self.pixelRange.indices(pix_len))

    def get_colors(self):
        return self.pixels[self.pixelRange]

    def set_colors(self, values: Union[Color, Iterable[Color]]):
        # TODO: optimize if needed
        pix_len = len(self.pixels)

        # NeoPixels require indexable values. if they're an iterator of colors and length is OK, simply set them.
        # Otherwise, enumerate them into a list and cycle them if there aren't enough
        if _is_multi_colors(values) and len(values) >= pix_len:
            self._set_colors(values)
        else:
            cycled_values = list(_get_cycled_colors(values, pix_len))
            self._set_colors(cycled_values)

    def _set_colors(self, values):
        self.pixels[self.pixelRange] = values

    def show(self):
        self.pixels.show()
