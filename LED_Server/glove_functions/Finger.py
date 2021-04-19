import asyncio
import time
from typing import Callable

from neopixel import NeoPixel
from tornado.ioloop import IOLoop

from LED_Server.glove_functions import GLOVE_HACKS
from Utils.color_util import RGBBytesColor


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
                 hand: int, finger: int, color: RGBBytesColor,
                 flashFunc: Callable[[NeoPixel, str], "GloveFingerFlashAction"],
                 holdAction: Callable[[NeoPixel, str], "LedAction"]):
        super().__init__(name, hand, finger)
        self.flashFunc = flashFunc
        self.btn_held = False
        self.tilt_held = False
        self.holdFlashFunc = holdAction
        self.color = color

    def on_tilt_down(self, pixels: NeoPixel):
        # print(f"[{self.name}] Tilt down")

        self.action = None
        self.tilt_held = False

        asyncio.create_task(self.tilt_hold_loop(pixels))

    def on_tilt_hold(self, pixels: NeoPixel):
        if not self.holdFlashFunc: return
        # print(f"[{self.name}] Tilt hold")

        self.action = self.holdFlashFunc(pixels, self.name)
        return self.action

    def on_tilt_up(self, pixels: NeoPixel):
        print(f"[{self.name}] Tilt up")
        action = self.flashFunc(pixels, self.name)
        self.action = action
        self.tilt_held = True
        return action

    def on_finger_down(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger down")
        GLOVE_HACKS.CURR_HAND_COLORS[self.hand] = self.color

    def on_finger_hold(self, pixels: NeoPixel):
        # print(f"[{self.name}] Finger hold")
        pass


    def on_finger_up(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger up")
        self.btn_held = False

    async def hold_loop(self, pixels: NeoPixel):
        last_call_timestamp = time.time()
        while self.btn_held:
            curTime = time.time()
            if curTime - last_call_timestamp > GLOVE_HACKS.FINGER_PRESS_COOLDOWN_MILLIS:
                self.on_finger_hold(pixels)
                last_call_timestamp = curTime
            await asyncio.sleep(0.200)

    async def tilt_hold_loop(self, pixels: NeoPixel):
        last_call_timestamp = time.time()
        while self.tilt_held:
            curTime = time.time()
            if curTime - last_call_timestamp > GLOVE_HACKS.FINGER_PRESS_COOLDOWN_MILLIS:
                action = self.on_tilt_hold(pixels)
                if action:
                    GLOVE_HACKS.router.add_action(action)
                last_call_timestamp = curTime
            await asyncio.sleep(0.200)
