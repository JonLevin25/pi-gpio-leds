import tornado.web
from tornado.ioloop import IOLoop

from LED_Server.event_loop import event_loop
from LED_Server.actions.action_routers.PixelsActionsRouter import PixelsActionsRouter
from LED_Server.actions.actions_service import ActionsService
from LED_Server.discovery.discovery_service import DiscoveryService
from CONSTS import *

from LED_Server.glove_functions import GLOVE_HACKS
from LED_Server.glove_functions.glove_helper import on_glove_finger_down, on_glove_finger_up, on_glove_finger_press

from led_actions.action_starters import *
from led_actions.actions.BaseColorLedAction import BaseColorLedAction
from led_actions.actions.BulgeLedAction import Bulge
import atexit

from led_actions.actions.FillGapsAction import FillGapsAction
from led_actions.base.LedAction import LedAction


def fill_gaps_action(pixels: NeoPixel, fill_length: int, gap_length: int) -> LedAction:
    set_colors_action = lambda: Actions_Basic.set_sequential(pixels, 0, 0.1)
    return FillGapsAction(pixels, set_colors_action,
                                    fill_length=fill_length, gap_length=gap_length, half_cycle_time=3,
                                    min_brightness=0.2, max_brightness=1.0)

def run_test_code(pixels: NeoPixel, router: PixelsActionsRouter):
    golden_yellow = html_to_rgb_bytes("#ff9900")
    lehe_jon_first_draw_theme = html_to_rgb_bytes("#33ccff")
    purple = html_to_rgb_bytes("#792d9f")

    pixels.brightness = 1

    ### ReadLight
    # Actions_Basic.set_range(pixels, slice(5, 10), (255, 180, 0))
    # pixels.brightness = 0.5
    # return


    router.add_actions([
        BaseColorLedAction(pixels, GLOVE_HACKS.BASE_COLOR)
        # fill_gaps_action(3, 2),
        # Actions_Breathe.bright_pingpong_2(pixels, 1.5),
        # Actions_ColorCycle.colorcylce(pixels, 6),
        # Bulge(3, pixels, START_COL, rand_deep_color, 0.0055),  # TODO: Easing
    ])


def init_app() -> Tuple[NeoPixel, PixelsActionsRouter]:
    print('initializing pixels')
    pixels = event_loop.init_pixels(30)
    router = PixelsActionsRouter(pixels, {
        'glove_finger_down': on_glove_finger_down,
        'glove_finger_press': on_glove_finger_press,
        'glove_finger_up': on_glove_finger_up,
        'brightness': set_brightness,
        'rand_color': test_fill_rand,
        'set_sequential': Actions_Basic.set_sequential,
        'color_cycle': Actions_ColorCycle.colorcylce,
        'fill_gaps_action': fill_gaps_action,
    },
        allow_multi_actions=True)

    run_test_code(pixels, router)
    atexit.register(lambda: on_app_exit(pixels))

    print(f'listening on port {PORT}')

    return pixels, router


def make_tornado_app(pixels: NeoPixel, router: PixelsActionsRouter):
    application = tornado.web.Application([
        (DISCOVERY_PATH, DiscoveryService, dict(actions_router=router)),
        (ACTIONS_PATH, ActionsService, dict(actions_router=router)),
        # (ACTIONS_PATH, WebSocketHandler, dict(actions_router=router)),
    ])

    application.listen(PORT)

    # start event loop
    lifecycle_coroutine = event_loop.start_pixels_lifecycle_async(router)
    IOLoop.current().run_sync(lambda: lifecycle_coroutine)


def on_app_exit(pixels):
    pixels.fill(COL_BLACK)
    pixels.show()
    print('Exiting...')


if __name__ == "__main__":
    pixels, router = init_app()
    make_tornado_app(pixels, router)
