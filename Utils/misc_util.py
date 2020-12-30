from math import ceil
from typing import Callable, Iterable

FnVoid = Callable[[], None]

def is_iter(obj):
    if obj is None:
        return False
    return getattr(obj, "__iter__", None) is not None

def slice_idx(s: slice, src_len: int, idx: int):
    NotImplemented
    i = 0
    try:
        for val in slice_idxs(s, src_len):
            if i == idx:
                return val
            i += 1

    # TODO: Is this what would be thrown?
    except StopIteration:
        raise

def slice_idxs(s: slice, src_len: int) -> Iterable[int]:
    stop = min(s.stop, src_len)
    yield from range(s.start, stop, s.step)

def max_slice_len(s: slice):
    assert s.stop or s.stop == 0, "Must define stop for max slice len!"
    assert s.step != 0, "Step slice cannot be zero"

    start = s.start or 0
    stop = s.stop
    step = s.step or 1

    delta = (stop - start)
    dsteps = int(ceil(delta / step))

    return dsteps if dsteps >= 0 else 0


def slice_len(s: slice, src_len: int):
    stop = min(s.stop, src_len)
    return max_slice_len(slice(s.start, stop, s.step))


