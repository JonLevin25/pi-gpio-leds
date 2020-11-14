def lerp(t: float, from_: float, to: float) -> float:
    delta = to - from_
    return from_ + t * delta


def inverse_lerp(t: float, from_: float, to: float) -> float:
    delta = to - from_
    if delta == 0:
        raise ValueError("_from and to cannot be the same!")
    return (t - from_) / delta


def lerp01(t: float) -> float:
    return lerp(t, 0.0, 1.0)


def inverse_lerp01(t: float) -> float:
    return inverse_lerp(t, 0.0, 1.0)