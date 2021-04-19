import asyncio
import time
from typing import Callable, List

from neopixel import NeoPixel
from tornado.ioloop import IOLoop

from LED_Server.glove_functions import GLOVE_HACKS
from Utils.color_util import RGBBytesColor, color_lerp_rgb

GloveFunc = Callable[[NeoPixel, str], "GloveFingerFlashAction"]

class Finger:
    def __init__(self, name: str, hand: int, finger: int):
        self.hand = hand
        self.finger = finger
        self.name = name
        self.actions: List['GloveFingerFlashAction'] = []

    def on_finger_down(self, pixels: NeoPixel):
        pass

    def on_finger_up(self, pixels: NeoPixel):
        pass


class FlashFinger(Finger):
    def __init__(self,
                 name: str,
                 hand: int, finger: int, color: RGBBytesColor,
                 flashFunc: GloveFunc,
                 holdAction: GloveFunc):
        super().__init__(name, hand, finger)
        self.flashFunc = flashFunc
        self.btn_held = False
        self.tilt_held = False
        self.holdFlashFunc = holdAction
        self.color = color

    ###
    # raw callbacks - can switch start/stop to invert
    def on_tilt_down(self, pixels: NeoPixel):
        print(f"[{self.name}] Tilt down")
        # return self.on_tilt_started(pixels)

    def on_tilt_up(self, pixels: NeoPixel):
        print(f"[{self.name}] Tilt up")
        return self.on_tilt_stopped(pixels)

    def on_finger_down(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger down")
        return self.on_btn_started(pixels)

    def on_finger_up(self, pixels: NeoPixel):
        print(f"[{self.name}] Finger up")
        return self.on_btn_stopped(pixels)

    # ###
    # # Main logic
    # def on_tilt_started(self, pixels: NeoPixel):
    #     self.tilt_held = True
    #     asyncio.create_task(self.tilt_hold_loop(pixels))
    #
    #
    # def on_tilt_hold(self, pixels: NeoPixel):
    #     # print(f"[{self.name}] Tilt hold")
    #     prev_color = GLOVE_HACKS.CURR_HAND_COLORS[self.hand]
    #     GLOVE_HACKS.CURR_HAND_COLORS[self.hand] = color_lerp_rgb(0.65, prev_color, self.color)
    #     # for action in self.actions:
    #     #     action.color = color_lerp_rgb(0.05, action.color, self.color)


    def on_tilt_stopped(self, pixels: NeoPixel):
        self.tilt_held = False


    def on_btn_started(self, pixels):
        self.btn_held = True
        action = self.start_action(self.flashFunc, pixels)

        asyncio.create_task(self.btn_hold_loop(pixels))
        return action

    def on_btn_hold(self, pixels: NeoPixel):
        # print(f"[{self.name}] Finger hold")
        return self.start_action(self.holdFlashFunc, pixels)

    def on_btn_stopped(self, pixels):
        self.btn_held = False


    def start_action(self, action_starter: GloveFunc, pixels: NeoPixel):
        if not action_starter: return

        action = action_starter(pixels, self.name)
        self.actions.append(action)

        print(f"[{self.name}] Started action {action}.")

        action.subscribe_to_destroy(self.on_action_destroyed)
        return action


    ###
    # Helpers
    async def btn_hold_loop(self, pixels: NeoPixel):
        last_call_timestamp = time.time()
        while self.btn_held:
            curTime = time.time()
            if curTime - last_call_timestamp > GLOVE_HACKS.FINGER_PRESS_COOLDOWN_SECS:
                action = self.on_btn_hold(pixels)
                if action:
                    GLOVE_HACKS.router.add_action(action)
                last_call_timestamp = curTime
            await asyncio.sleep(0.200)

    async def tilt_hold_loop(self, pixels: NeoPixel):
        last_call_timestamp = time.time()
        while self.tilt_held:
            curTime = time.time()
            if curTime - last_call_timestamp > GLOVE_HACKS.FINGER_PRESS_COOLDOWN_SECS:
                action = self.on_tilt_hold(pixels)
                if action:
                    GLOVE_HACKS.router.add_action(action)
                last_call_timestamp = curTime
            await asyncio.sleep(0.200)


    def on_action_destroyed(self, action: 'LedAction'):
        try:
            self.actions.remove(action)
        except ValueError as e:
            print(f"[{self.name}] ERROR: Tried to remove {action} but it wasn't in list!")
