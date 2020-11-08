import RPi.GPIO as GPIO
import time

RED_GPIO = 24
GREEN_GPIO = 23
BLUE_GPIO = 18

all_channels = [RED_GPIO, GREEN_GPIO, BLUE_GPIO]

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

for channel in all_channels:
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)


def set_all(val):
    for channel in all_channels:
        GPIO.output(channel, val)


# Generator that will turn on the next color each time
def color_gen(amount=-1):
    c1 = 0
    c2 = 1
    while amount != 0:
        print("({0})".format(c1))
        yield (all_channels[c1])
        print("({}, {})".format(c1, c2))
        yield (all_channels[c1], all_channels[c2])

        # reset and increment lights (light 1 will have old light 2 value)
        GPIO.output(all_channels[c2], False)
        c1 = (c1 + 1) % len(all_channels)
        c2 = (c2 + 1) % len(all_channels)

        if amount > 0:
            amount -= 1


# hack to skip the second combination of colors (red/green) since it just looks green)
def color_gen_hack(amount=-1):
    inner_gen = color_gen(amount)
    i = -1
    for c in inner_gen:
        i = (i + 1) % (len(all_channels) * 3)

        if i in (1, 2):
            continue
        yield c


def flash(pins, secs):
    GPIO.output(pins, True)
    time.sleep(secs)
    GPIO.output(pins, False)


def cycle(sleep_delta, count=1):
    for pins in color_gen(count * len(all_channels)):
        flash(pins, sleep_delta)


def morse(text, dash_len=0.9, dot_len=0.2, letter_sep_len=0.5, word_sep_len=1):
    DOT = 0
    DASH = 1

    ascii_to_morse = {
        'A': (DOT, DASH,),
        'B': (DASH, DOT, DOT, DOT,),
        'C': (DASH, DOT, DASH, DOT,),
        'D': (DASH, DOT, DOT,),
        'E': (DOT,),
        'F': (DOT, DOT, DASH, DOT,),
        'G': (DASH, DASH, DOT,),
        'H': (DOT, DOT, DOT, DOT,),
        'I': (DOT, DOT,),
        'J': (DOT, DASH, DASH, DASH,),
        'K': (DASH, DOT, DASH,),
        'L': (DOT, DASH, DOT, DOT,),
        'M': (DASH, DASH,),
        'N': (DASH, DOT,),
        'O': (DASH, DASH, DASH,),
        'P': (DOT, DASH, DASH, DOT,),
        'Q': (DASH, DASH, DOT, DASH,),
        'R': (DOT, DASH, DOT,),
        'S': (DOT, DOT, DOT,),
        'T': (DASH,),
        'U': (DOT, DOT, DASH,),
        'V': (DOT, DOT, DOT, DASH,),
        'W': (DOT, DASH, DASH,),
        'X': (DASH, DOT, DOT, DASH,),
        'Y': (DASH, DOT, DASH, DASH,),
        'Z': (DASH, DASH, DOT, DOT,),
        '1': (DOT, DASH, DASH, DASH, DASH,),
        '2': (DOT, DOT, DASH, DASH, DASH,),
        '3': (DOT, DOT, DOT, DASH, DASH,),
        '4': (DOT, DOT, DOT, DOT, DASH,),
        '5': (DOT, DOT, DOT, DOT, DOT,),
        '6': (DASH, DOT, DOT, DOT, DOT,),
        '7': (DASH, DASH, DOT, DOT, DOT,),
        '8': (DASH, DASH, DASH, DOT, DOT,),
        '9': (DASH, DASH, DASH, DASH, DOT,),
        '0': (DASH, DASH, DASH, DASH, DASH,),
        ', ': (DASH, DASH, DOT, DOT, DASH, DASH,),
        '.': (DOT, DASH, DOT, DASH, DOT, DASH,),
        '?': (DOT, DOT, DASH, DASH, DOT, DOT,),
        '/': (DASH, DOT, DOT, DASH, DOT,),
        '-': (DASH, DOT, DOT, DOT, DOT, DASH,),
        '(': (DASH, DOT, DASH, DASH, DOT),
        ')': (DASH, DOT, DASH, DASH, DOT, DASH)
    }

    def get_flash_len(symbol):
        if symbol == DOT:
            return dot_len * 0.5
        elif symbol == DASH:
            return dash_len * 0.5
        else:
            raise ValueError

    def handle_letter(pins, morse_symbols):
        for symbol in morse_symbols:
            flash_len = get_flash_len(symbol)
            flash(pins, flash_len)
            time.sleep(flash_len * 1)
            # time.sleep(symbol_sep_len)
        time.sleep(letter_sep_len)

    # COLOR CYCLE
    cgen = color_gen()

    # GREEN ONLY
    # cgen = (green for x in iter(int, 1))

    colors = next(cgen)
    for c in (x.upper() for x in text):
        if c.isspace():
            time.sleep(word_sep_len - letter_sep_len)
        elif c in ascii_to_morse:
            handle_letter(colors, ascii_to_morse[c])
        else:
            raise ValueError
        colors = next(cgen)


def main():
    try:
        # cycle(0.4, 5)
        morse("Fuck you")
        # flash(red, 2)
        # flash(green, 2)
        # flash(blue, 2)
        # cycle(0.5, 3)
    finally:
        set_all(False)
        GPIO.cleanup()


if __name__ == '__main__':
    main()