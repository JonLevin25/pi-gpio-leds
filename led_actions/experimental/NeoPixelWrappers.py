import typing
from operator import __getitem__

from adafruit_pypixelbuf import PixelBuf
from neopixel import NeoPixel
import itertools
from typing import Union, Iterable, Sized, Iterator, List, Tuple

from Utils.color_util import RGBBytesColor
from Utils.misc_util import slice_len, slice_idx, slice_idxs

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


### Python 3.8+ only
#
# class IColorBuffer(Protocol):
#     def __len__(self):
#         pass
#     def __getitem__(self, index) -> any:
#         pass
#     def __setitem__(self, index, value: any) -> None:
#         pass

class NeoPixelRange:
    """
    A simple yet powerful indirection for storing pixel info.
    Can hold an array for later usage/blending, a NeoPixelRange that
    """
    def __init__(self, inner_buffer: Union["NeoPixelRange", PixelBuf, List[RGBBytesColor]], range_slice: slice = None):
        if not inner_buffer:
            raise ValueError('No inner buffer given!')

        self._inner_buffer = inner_buffer
        self.range_slice = range_slice or slice(None)

    def __len__(self):
        inner_len = len(self._inner_buffer)
        return slice_len(self.range_slice, inner_len)

    def __getitem__(self, index: Union[int, slice]) -> RGBBytesColor:
        if type(index) == int:
            return self._get_idx(index)
        else:
            NotImplemented



    ## TODO: Not working - Impl this properly
    def __setitem__(self, index: Union[int, slice], val: Union[RGBBytesColor, List[RGBBytesColor]]):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            for i, idx_i in enumerate(range(start, stop, step)):
                pass # TODO
        else:
            r, g, b, w = self._parse_color(val)
            self._set_item(index, r, g, b, w)

    def _get_idx(self, index: int):
        return slice_idx(self.range_slice, len(self), index)

    def get_colors(self):
        return self._inner_buffer[self.range_slice]

    # TODO: Getitem

    def set_colors(self, values: Union[Color, Iterable[Color]]):
        # TODO: optimize if needed
        pix_len = len(self._inner_buffer)

        # NeoPixels require indexable values. if they're an iterator of colors and length is OK, simply set them.
        # Otherwise, enumerate them into a list and cycle them if there aren't enough
        if _is_multi_colors(values) and len(values) >= pix_len:
            self._set_colors(values)
        else:
            cycled_values = list(_get_cycled_colors(values, pix_len))
            self._set_colors(cycled_values)

    def _set_colors(self, values):
        self._inner_buffer[self.range_slice] = values

    def show(self):
        self._inner_buffer.show()