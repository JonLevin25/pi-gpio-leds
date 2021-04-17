import asyncio
from typing import Callable

from neopixel import NeoPixel
from tornado.ioloop import IOLoop


class Finger:
    def __init__(self,
                 hand: int, finger: int,
                 name: str,
                 holdable: bool):
        self.hand = hand
        self.finger = finger
        self.holdable = holdable
        self.name = name
        self.action = None

    def on_finger_down(self, pixels: NeoPixel):
        pass

    def on_finger_up(self, pixels: NeoPixel):
        pass


class FlashFinger(Finger):
    def __init__(self,
                 hand: int, finger: int,
                 flashFunc: Callable[[NeoPixel, str], "GloveFingerFlashAction"],
                 name: str,
                 holdable: bool):
        super().__init__(hand, finger, name, holdable)
        self.flashFunc = flashFunc
        self.is_pressed = False

    def on_finger_down(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger down")
        action = self.flashFunc(pixels, self.name)
        self.action = action
        self.is_pressed = True
        # asyncio.create_task(self.finger_press_loop(pixels))
        return action

    # Get finger press from glove
    # async def finger_press_loop(self, pixels: NeoPixel):
    #     while self.is_pressed:
    #         await asyncio.sleep(0.200)
    #         self.on_finger_press(pixels)


    def on_finger_press(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger press")
        if not self.action: return


    def on_finger_up(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger up")
        #
        self.action = None
        self.is_pressed = False
