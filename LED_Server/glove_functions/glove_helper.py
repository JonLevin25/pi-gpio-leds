from neopixel import NeoPixel

HAND_LEFT = 0
HAND_RIGHT = 1

FINGER_IDX = 0
FINGER_MID = 1
FINGER_RING = 2
FINGER_PINKY = 3
# FINGER_THUMB = 4

# TODO: Return LedAction
def index_finger(pixels):
    print("INDEX FINGER!")

def middle_finger(pixels):
    print('MIDDLE FINGER!')

fn_dict = {
    (HAND_LEFT, FINGER_IDX): index_finger,
    (HAND_LEFT, FINGER_MID): middle_finger,
    (HAND_LEFT, FINGER_RING): None,
    (HAND_LEFT, FINGER_PINKY): None,

    (HAND_RIGHT, FINGER_IDX): None,
    (HAND_RIGHT, FINGER_MID): None,
    (HAND_RIGHT, FINGER_RING): None,
    (HAND_RIGHT, FINGER_PINKY): None,
}

def glove_request_handler(pixels: NeoPixel, hand: int, finger: int):
    return fn_dict[(hand, finger)](pixels)
