import machine
import neopixel
import math
import time

# =====================================
# CONFIGURATION
# =====================================

PIN = 28
WIDTH = 16
HEIGHT = 16
NUM_LEDS = WIDTH * HEIGHT

# Limitation de luminosité
BRIGHTNESS = 0.1

np = neopixel.NeoPixel(
    machine.Pin(PIN),
    NUM_LEDS
)

# =====================================
# ZIGZAG
# =====================================

def xy_to_index(x, y):

    if y % 2 == 0:
        return y * WIDTH + x

    return y * WIDTH + (WIDTH - 1 - x)

# =====================================
# LIMITATION COURANT
# =====================================

def scale(r, g, b):

    return (
        int(r * BRIGHTNESS),
        int(g * BRIGHTNESS),
        int(b * BRIGHTNESS)
    )

# =====================================
# PALETTE ARC-EN-CIEL
# =====================================

def wheel(pos):

    pos = pos % 256

    if pos < 85:
        return (
            255 - pos * 3,
            pos * 3,
            0
        )

    if pos < 170:

        pos -= 85

        return (
            0,
            255 - pos * 3,
            pos * 3
        )

    pos -= 170

    return (
        pos * 3,
        0,
        255 - pos * 3
    )

# =====================================
# PIXEL
# =====================================

def set_pixel(x, y, color):

    if 0 <= x < WIDTH and 0 <= y < HEIGHT:

        r, g, b = color

        np[xy_to_index(x, y)] = scale(r, g, b)

# =====================================
# PLASMA
# =====================================

t = 0.0

while True:

    for y in range(HEIGHT):

        for x in range(WIDTH):

            v = 0

            v += math.sin(x / 2.0 + t)
            v += math.sin(y / 3.0 + t)

            v += math.sin(
                (x + y) / 4.0 + t
            )

            v += math.sin(
                math.sqrt(
                    (x - 8) ** 2 +
                    (y - 8) ** 2
                ) / 2.0 + t
            )

            color_index = int(
                (v + 4) * 32
            )

            set_pixel(
                x,
                y,
                wheel(color_index)
            )

    np.write()

    t += 0.15

    time.sleep(0.02)