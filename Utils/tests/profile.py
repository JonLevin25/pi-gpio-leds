import datetime
import timeit

from gpiozero.tools import averaged

from Utils.misc_util import max_slice_len, max_slice_len_2

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

def test_1():
    for (s, expected) in simple_test_cases:
        assert max_slice_len(s) == expected


def test_2():
    for (s, expected) in simple_test_cases:
        assert max_slice_len_2(s) == expected

def avg(l):
    return sum(l) / len(l)

num = 1_000_000_000
repeat=5

start = datetime.datetime.now()
res1 = timeit.repeat('test', number=num, repeat=repeat, globals={"test": test_1})
res2 = timeit.repeat('test', number=num, repeat=repeat, globals={"test": test_2})
end = datetime.datetime.now()

a1 = avg(res1)
a2 = avg(res2)

print(f"Total time taken: {end - start}")
print(f"1: {a1}. 2: {a2}. delta: {a2 - a1}")