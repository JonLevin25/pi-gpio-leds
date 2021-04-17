import asyncio
import time
from typing import Callable

from neopixel import NeoPixel
from tornado.ioloop import IOLoop

from LED_Server.glove_functions import GLOVE_HACKS


class Finger:
    def __init__(self, name: str, hand: int, finger: int):
        self.hand = hand
        self.finger = finger
        self.name = name
        self.action = None

    def on_finger_down(self, pixels: NeoPixel):
        pass

    def on_finger_up(self, pixels: NeoPixel):
        pass


class FlashFinger(Finger):
    def __init__(self,
                 name: str,
                 hand: int, finger: int,
                 flashFunc: Callable[[NeoPixel, str], "GloveFingerFlashAction"],
                 holdAction: Callable[[NeoPixel, str], "LedAction"]):
        super().__init__(name, hand, finger)
        self.flashFunc = flashFunc
        self.is_pressed = False
        self.last_press_timestamp = -9999
        self.holdFlashFunc = holdAction

    def on_finger_down(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger down")
        action = self.flashFunc(pixels, self.name)
        self.action = action
        self.is_pressed = True
        self.last_press_timestamp = time.time()
        return action

    def on_finger_press(self, pixels: NeoPixel):
        if not self.holdFlashFunc: return

        curTime = time.time()
        if curTime - self.last_press_timestamp < GLOVE_HACKS.FINGER_PRESS_COOLDOWN:
            return

        print(f"[{self.name}] Finger press")
        self.action = self.holdFlashFunc(pixels, self.name)
        self.last_press_timestamp = curTime
        return self.action


    def on_finger_up(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger up")
        #
        self.action = None
        self.is_pressed = False
