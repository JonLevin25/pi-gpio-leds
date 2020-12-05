import unittest
from led_actions.NeoPixelRange import NeoPixelRange
from led_actions.NeoPixelTween import *


class TestGenericTween(unittest.TestCase):
    def test_tweento_ints_linear(self):
        tweened_value = 0

        getter = lambda: tweened_value

        def setter(val):
            nonlocal tweened_value
            tweened_value = val

        tween = TweenTo(getter, setter, 100, 10, unit_value=1)

        tween.start(0)
        assert tweened_value == 0
        val_expected = (
            (0, 0),
            (1, 10),
            (1.55, 15.5),
            (5, 50),
            (9.99, 99.9),
            (10, 100),
            (10.0, 100),
            (1, 10),  # can go back, delta should adjust
            (11, 110)
        )

        for (val, expected) in val_expected:
            tween.update(val)
            assert tweened_value == expected, "Tweened duration: {} -> Expected {}. was: {}" \
                .format(val, expected, tweened_value)


if __name__ == '__main__':
    unittest.main()
