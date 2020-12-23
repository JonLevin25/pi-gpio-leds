from typing import Union, TypeVar

FloatOrInt = TypeVar('FloatOrInt', int, float)


def lerpFloat(t: float, from_: float, to: float) -> float:
    delta = to - from_
    return from_ + t * delta


def lerpInt(t: float, from_: int, to: int) -> int:
    result = lerpFloat(t, from_, to)
    return int(result)


def inverse_lerp(t: float, from_: float, to: float) -> float:
    delta = to - from_
    if delta == 0:
        raise ValueError("_from and to cannot be the same!")
    return (t - from_) / delta


def lerp01(t: float) -> float:
    return lerpFloat(t, 0.0, 1.0)


def inverse_lerp01(t: float) -> float:
    return inverse_lerp(t, 0.0, 1.0)


def clampFloat(value: float, floor_val: float, ceil_val: float):
    if value < floor_val:
        return floor_val
    elif value > ceil_val:
        return ceil_val
    return value


def clampInt(value: int, floor_val: int, ceil_val: int):
    if value < floor_val:
        return floor_val
    elif value > ceil_val:
        return ceil_val
    return value
