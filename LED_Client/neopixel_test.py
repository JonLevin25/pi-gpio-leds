import event_loop
from LEDActionsHandler import *

def main(pixels: NeoPixel):
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

    print('creating actions to run')

    # Actions_Basic.set_random(pixels, rand_func_max_colors(3, rand_deep_color))
    Actions_Basic.set_sequential(pixels)

    set_colors_action = lambda: Actions_Basic.set_sequential(pixels, 0, 0.1)
    # fillgapsaction = FillGapsAction(pixels, set_colors_action,
    #                                 fill_length=3,
    #                                 gap_length=1,
    #                                 half_cycle_time=0.2,
    #                                 min_brightness=0.2,
    #                                 max_brightness=1.0,
    #                                 on_halfcycle=None)

    actions = [
        # fillgapsaction
        # Actions_Breathe.bright_pingpong_2(pixels, 1.5),
        Actions_ColorCycle.colorcylce(pixels,6),
        # Bulge(3, pixels, START_COL, rand_deep_color, 0.0055), # TODO: Easing
    ]

    event_loop.run_loop(pixels, actions)


##########
#############
#########

new_pixels = event_loop.init_pixels(30)
try:
    main(new_pixels)
    while True:
        pass  # just here to prototype stuff instead of main quickly
finally:
    new_pixels.fill(COL_BLACK)
    new_pixels.show()
    print('Exiting...')
