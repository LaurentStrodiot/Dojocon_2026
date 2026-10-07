import machine
import neopixel
import random
import time

PIN = 28
WIDTH = 16
HEIGHT = 16
NUM_LEDS = WIDTH * HEIGHT
BRIGHTNESS = 0.1

np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)

board = [[(0,0,0) for _ in range(WIDTH)] for _ in range(HEIGHT)]

SHAPES = [
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[0,1,0],[1,1,1]],
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]],
    [[1,1,0],[0,1,1]],
    [[0,1,1],[1,1,0]]
]

COLORS = [
    (0,255,255),
    (255,255,0),
    (255,0,255),
    (255,128,0),
    (0,0,255),
    (0,255,0),
    (255,0,0)
]

def limit_color(c):
    return (
        int(c[0] * BRIGHTNESS),
        int(c[1] * BRIGHTNESS),
        int(c[2] * BRIGHTNESS)
    )

def xy_to_index(x, y):
    if y % 2 == 0:
        return y * WIDTH + x
    return y * WIDTH + (WIDTH - 1 - x)


def clear_matrix():
    for i in range(NUM_LEDS):
        np[i] = (0,0,0)


def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        np[xy_to_index(x, y)] = limit_color(color)


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def new_piece():
    idx = random.randint(0, len(SHAPES)-1)
    shape = SHAPES[idx]
    color = COLORS[idx]
    for _ in range(random.randint(0,3)):
        shape = rotate(shape)
    return shape, color


def collision(shape, px, py):
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                bx = px + x
                by = py + y
                if bx < 0 or bx >= WIDTH:
                    return True
                if by >= HEIGHT:
                    return True
                if by >= 0 and board[by][bx] != (0,0,0):
                    return True
    return False


def merge(shape, px, py, color):
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                bx = px + x
                by = py + y
                if 0 <= by < HEIGHT:
                    board[by][bx] = color


def render_static():
    clear_matrix()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            c = board[y][x]
            if c != (0,0,0):
                set_pixel(x,y,c)
    np.write()


def clear_lines():
    global board
    rows = []
    for y in range(HEIGHT):
        if all(board[y][x] != (0,0,0) for x in range(WIDTH)):
            rows.append(y)

    if not rows:
        return

    for _ in range(3):
        for row in rows:
            for x in range(WIDTH):
                board[row][x] = (80,80,80)
        render_static()
        time.sleep(0.08)

        for row in rows:
            for x in range(WIDTH):
                board[row][x] = (0,0,0)
        render_static()
        time.sleep(0.08)

    for row in reversed(rows):
        del board[row]

    while len(board) < HEIGHT:
        board.insert(0, [(0,0,0) for _ in range(WIDTH)])


def render(shape, px, py, color):
    clear_matrix()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            c = board[y][x]
            if c != (0,0,0):
                set_pixel(x,y,c)

    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                set_pixel(px+x, py+y, color)

    np.write()


def game_over_flash():
    red = limit_color((255,0,0))
    for _ in range(3):
        for i in range(NUM_LEDS):
            np[i] = red
        np.write()
        time.sleep(0.2)
        clear_matrix()
        np.write()
        time.sleep(0.2)

while True:
    shape, color = new_piece()

    px = WIDTH // 2 - len(shape[0]) // 2
    py = 0
    drift = random.choice([-1,0,1])

    if collision(shape, px, py):
        game_over_flash()
        board = [[(0,0,0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
        continue

    falling = True

    while falling:
        render(shape, px, py, color)
        time.sleep(0.12)

        if random.randint(0,5) == 0:
            nx = px + drift
            if not collision(shape, nx, py):
                px = nx

        if collision(shape, px, py + 1):
            merge(shape, px, py, color)
            clear_lines()
            falling = False
        else:
            py += 1
