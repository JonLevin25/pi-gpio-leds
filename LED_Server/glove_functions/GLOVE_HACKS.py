from LED_Server.actions.action_routers.PixelsActionsRouter import PixelsActionsRouter
from Utils.color_util import *

HAND_LEFT = 0
HAND_RIGHT = 1

FINGER_IDX = 0
FINGER_MID = 1
FINGER_RING = 2
FINGER_PINKY = 3
# FINGER_THUMB = 4

router: PixelsActionsRouter
BASE_COLOR = (127, 127, 127)
FAST_LED_DELTA = 0.05
FAST_LED_ANIM_TIME = 0.3

FINGER_PRESS_COOLDOWN_SECS = 0.15



IDX_FINGER_COL = COL_RED
MID_FINGER_COL = COL_GREEN
RING_FINGER_COL = COL_BLUE
# COLOR_PINKY = COL_YELLOW

def leftColor():
    return CURR_HAND_COLORS[HAND_LEFT]

def rightColor():
    return CURR_HAND_COLORS[HAND_RIGHT]

CURR_HAND_COLORS = [
    COL_RED, # Left
    COL_RED, # Right
]