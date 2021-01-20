import tornado.web
from tornado.ioloop import IOLoop

import event_loop
from LED_Server.actions.action_routers.PixelsActionsRouter import PixelsActionsRouter
from LED_Server.actions.actions_service import ActionsService
from LED_Server.discovery.discovery_service import DiscoveryService
from CONSTS import *

from led_actions.action_starters import *
from led_actions.actions.BulgeLedAction import Bulge


def init() -> PixelsActionsRouter:
    print('initializing pixels')
    pixels = event_loop.init_pixels(30)

    golden_yellow = html_to_rgb_bytes("#ff9900")
    lehe_jon_first_draw_theme = html_to_rgb_bytes("#33ccff")
    purple = html_to_rgb_bytes("#792d9f")
    START_COL = purple

    Actions_Basic.autoshow(pixels, True)

    ### ReadLight
    # Actions_Basic.set_range(pixels, slice(5, 10), (255, 180, 0))
    # pixels.brightness = 0.5
    # return

    pixels.brightness = 1
    pixels.fill(START_COL)

    # prange = NeoPixelRange(pixels, slice(3, len(pixels), 4))
    # prange.set_colors(COL_BLACK)
    # prange.show()

    # Actions_Basic.set_random(pixels, rand_func_max_colors(3, rand_deep_color))
    Actions_Basic.set_sequential(pixels)

    router = PixelsActionsRouter(pixels, {
        'brightness': set_brightness,
        'rand_color': test_fill_rand,
        'set_sequential': Actions_Basic.set_sequential,
        'color_cycle': Actions_ColorCycle.colorcylce,
    })

    # set_colors_action = lambda: Actions_Basic.set_sequential(pixels, 0, 0.1)
    # fillgapsaction = FillGapsAction(pixels, set_colors_action,
    #                                 fill_length=3,
    #                                 gap_length=1,
    #                                 half_cycle_time=0.2,
    #                                 min_brightness=0.2,
    #                                 max_brightness=1.0,
    #                                 on_halfcycle=None)

    router.running_actions = [
        #fillgapsaction,
        # Actions_Breathe.bright_pingpong_2(pixels, 1.5),
        # Actions_ColorCycle.colorcylce(pixels, 6),
        Bulge(3, pixels, START_COL, rand_deep_color, 0.0055), # TODO: Easing
    ]

    return router

def make_app():
    router = init()
    application = tornado.web.Application([
        (DISCOVERY_PATH, DiscoveryService, dict(actions_router=router)),
        (ACTIONS_PATH, ActionsService, dict(actions_router=router)),
        # (ACTIONS_PATH, WebSocketHandler, dict(actions_router=router)),
    ])

    application.listen(PORT)
    print(f'listening on port {PORT}')
    ioloop = IOLoop.current()
    ioloop.run_sync(lambda: event_loop.loop(router.pixels, router.running_actions))
    ioloop.start()

if __name__ == "__main__":
    make_app()