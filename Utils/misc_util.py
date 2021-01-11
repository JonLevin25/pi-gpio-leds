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


def reslice(orig_slice: slice, s2: slice, src_len):
    """Slice an existing slice such that using the return value should yield the same result as slicing them one after the other"""

    s1_start, s1_stop, s1_step = orig_slice.indices(src_len)
    s2_start, s2_stop, s2_step = s2.indices(src_len)

    start = s1_start + s1_step * s2_start
    stop = min(s1_stop, s2_stop)
    step = s1_step * s2_step

    return slice(start, stop, step)


def slice_idxs(s: slice, src_len: int) -> Iterable[int]:
    stop = min(s.stop, src_len)
    yield from range(s.start, stop, s.step)


def max_slice_len(start: int, stop: int, step: int):
    assert stop or stop == 0, "Must define stop for max slice len!"
    assert step != 0, "Step slice cannot be zero"

    start = start or 0
    stop = stop
    step = step or 1

    # handle negative
    start = start if start >= 0 else -start

    delta = (stop - start)
    dsteps = int(ceil(delta / step))

    return dsteps if dsteps >= 0 else 0


def slice_len(s: slice, src_len: int):
    indices = s.indices(src_len)
    print(indices)
    return max_slice_len(*indices)
