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


class NewRangeSketch(object):
    @classmethod
    def PixelWrapper(cls, pixels: NeoPixel) -> 'NewRangeSketch':
        return NewRangeSketch()

    @classmethod
    def TempBufferWrapper(cls, buffer: List) -> 'NewRangeSketch':
        pass

    @classmethod
    def WrapperWrapper(cls, wrapper: 'NewRangeSketch') -> 'NewRangeSketch':
        pass

    def __init__(self):
        pass


# TODO: Sort out code/API duplication (NeoPixelBuffer/NeoPixelRange)
class NeoPixelBuffer:
    def __init__(self, len_pixels: int, pixel_range: Union[int, slice] = None):
        if not len_pixels:
            raise ValueError('No pixel length given!')
        if pixel_range is None:
            pixel_range = slice(None, None)  # entire range
        if not isinstance(pixel_range, (int, slice)):
            raise ValueError('Pixel indices must be an int or a slice!')

        self.buffer_len = len_pixels
        self.pixelRange = pixel_range if isinstance(pixel_range, slice) else slice(0, pixel_range)

    def set_range_buffer(self, values: Union[Color, Iterable[Color]]):
        self._set_buffer(self.buffer_len, values)

    def get_all_pixels(self) -> List[Color]:
        values = [None for i in range(self.buffer_len)]  # type: List[any]
        values[self.pixelRange] = self._buffer
        return values

    def _set_buffer(self, buffer_len, values: Union[Color, Iterable[Color]]):
        # TODO: optimize if needed

        # NeoPixels require indexable values. if they're an iterator of colors and length is OK, simply set them.
        # Otherwise, enumerate them into a list and cycle them if there aren't enough
        if _is_multi_colors(values) and len(values) >= buffer_len:
            self._buffer = values[:buffer_len]
        else:
            cycled_values = list(_get_cycled_colors(values, buffer_len))
            self._buffer = cycled_values


# TODO: Sort out code/API duplication (NeoPixelBuffer/NeoPixelRange)
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

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._pixels)
            for val_i, in_i in enumerate(range(start, stop, step)):
                r, g, b, w = self._parse_color(val[val_i])
                self._set_item(in_i, r, g, b, w)
        else:
            r, g, b, w = self._parse_color(val)
            self._set_item(index, r, g, b, w)

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
