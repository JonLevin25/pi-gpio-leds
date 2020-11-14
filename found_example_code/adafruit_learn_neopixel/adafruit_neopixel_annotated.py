# Found at https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel
# Just for reference / learning. Changed a bit + added comments to study differences

# CircuitPython demo - NeoPixel
import time


# segments [0,255] range to 3 parts. Each part has:
# * Falling color - starts full (255), falls by pos*3 until empty (0)
# * Rising color - starts empty (0), rises by pos*3 until full (255)
# * Null color - always zero for segment
# * The cycle for any given color is [Fall, Null, Rise, Fall, ...]

# The semgents:
#  * [0, 85]    R: Falling, G: Rising,  B: Null
#  * [86, 170]  R: Null,    G: Falling: B: Rising
#  * [171, 255] R: Rising,  G: Null,    B: Falling
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


# added pixels param
def color_chase(pixels, color, wait):
    num_pixels = len(pixels)
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


# renames, pixels param
def rainbow_cycle(pixels, wait):
    for offset in range(255):
        set_pixels_sequential(pixels, offset)
        pixels.show()
        time.sleep(wait)


# extracted from rainbow_cycle to better sim logic
def set_pixels_sequential(pixels, offset):
    num_pixels = len(pixels)
    for i in range(num_pixels):
        # normalized pos in bytes (i.e. if u have 20 leds, Led#10 will be (0.5 * 255)
        rc_index_1 = (i * 256 // num_pixels)

        rc_index_2 = rc_index_1 + offset

        # x & 255 is basically x mod 256, since it discards all bits after that.
        # This is what makes it wrap around
        pixels[i] = wheel(rc_index_2 & 255)
