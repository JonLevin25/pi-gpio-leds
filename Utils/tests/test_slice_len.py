import unittest

from Utils.misc_util import slice_len, max_slice_len

class TestSliceUtil(unittest.TestCase):
    def test_max_len_suite(self):
        simple_test_cases = [
            (slice(0, 10, 1), 10),
            (slice(0, 10, 2), 5),
            (slice(0, 10, 3), 4),
            (slice(0, 10, 10), 1),
            (slice(0, 10, 100), 1),
            (slice(-1, 10, 5), 3),
            (slice(-10, -1, 3), 3),
            (slice(15, 10, 1), 0),
            (slice(0, 10, -1), 0),
            (slice(0, 10, -3), 0),
            (slice(15, 10, -1), 5),
            (slice(10, 0, -1), 10),

            # none replacement (without len)
            (slice(None, 10, 1), 10),
            (slice(0, 10, None), 10),
        ]

        full_cases = [
            (slice(0, 10, 1), 5, 5),
            (slice(0))
        ]

        def test_len(s: slice, expected_len: int):
            iter_len = s.stop + 1  # simulate some iterable that is longer than the max_len

            enumerated_idxs = list(range(s.start or 0, s.stop, s.step or 1))
            enumerated_len = len(enumerated_idxs)

            result = slice_len(s, iter_len)
            self.assertEqual(result, expected_len, "Not same as expected!")
            self.assertEqual(result, enumerated_len, "Not same as enumerated!")

        def test_max_len(s: slice, expected_len: int):
            result = max_slice_len(s)
            self.assertEqual(result, expected_len,
                             "Max len was not equal! slice: {}. expected: {}. Actual: {}".format(s, expected_len,
                                                                                                 result))
        for case in simple_test_cases:
            s, expected = case
            with self.subTest("max_len {} -> {}".format(s, expected)):
                test_max_len(s, expected)
            with self.subTest("len vs enumerated {} -> {}".format(s, expected)):
                test_len(s, expected)
