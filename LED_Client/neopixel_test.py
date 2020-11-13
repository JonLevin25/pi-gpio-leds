import math

import board
import neopixel
import time

# Colors
COL_BLACK = (0, 0, 0)
COL_BLUE = (0, 255, 0)
COL_RED = (255, 0, 0)

pixels = neopixel.NeoPixel(board.D18, 25, brightness=0.1, auto_write=False)

pixels.fill(COL_BLACK)
pixels.show()


def brightnessPingPong(minBright, maxBright, tick_millis=20, start_ascending=True):
    # clamp brightness to avoid getting stuck
    minBright = max(minBright, 0.01)
    maxBright = min(maxBright, 0.99)

    ascending = start_ascending
    bright_delta = 0.05
    milliToSecs = 0.001

    def should_switch(b):
        return b >= maxBright if ascending else b <= minBright

    def next_val(b):
        return b + bright_delta if ascending else b - bright_delta

    def next_target_time(t):
        return t + tick_millis * milliToSecs

    target_time = next_target_time(time.time())
    while True:
        currtime = time.time()
        if currtime < target_time:
            continue

        target_time = next_target_time(target_time)
        curr_bright = pixels.brightness
        print(curr_bright)
        if should_switch(curr_bright):
            ascending = not ascending

        new_bright = next_val(curr_bright)
        pixels.brightness = new_bright
        pixels.show()


try:
    pixels.brightness = 0
    pixels.fill(COL_BLUE)
    brightnessPingPong(0, 1, start_ascending=True)
finally:
    pixels.fill(COL_BLACK)
    pixels.show()
