from enum import Enum

import pyglet
from PIL import Image

from helpers import replace_color, get_pyglet_img_from_pil_image, \
    get_all_head_pics_from_head_n

blue_colors = [(40, 40, 255), (0, 38, 255), (62, 255, 48)]  # head, sides, eyes
red_colors = [(255, 40, 40), (255, 0, 38), (66, 255, 214)]
yellow_colors = [(255, 216, 0), (216, 216, 40), (255, 0, 0)]

b_head_n = Image.open("img/blue_head.png")
r_head_n = replace_color(b_head_n, blue_colors, red_colors)
y_head_n = replace_color(b_head_n, blue_colors, yellow_colors)

b_body = Image.open("img/blue_body.png")
r_body = replace_color(b_body, blue_colors, red_colors)
y_body = replace_color(b_body, blue_colors, yellow_colors)

blue_body_pic = get_pyglet_img_from_pil_image(b_body)
red_body_pic = get_pyglet_img_from_pil_image(r_body)
yellow_body_pic = get_pyglet_img_from_pil_image(y_body)

blue_head_pics = get_all_head_pics_from_head_n(b_head_n)
red_head_pics = get_all_head_pics_from_head_n(r_head_n)
yellow_head_pics = get_all_head_pics_from_head_n(y_head_n)

apple_pic = pyglet.image.load("img/apple.png")

painted_body_parts = [(yellow_body_pic, yellow_head_pics),
                      (red_body_pic, red_head_pics),
                      (blue_body_pic, blue_head_pics)]

SCALE_X = 1
SCALE_Y = 1
SPAWNED_SNAKES = 2
PLAYERS = 2
BLOCK_SIZE = (10, 10)
k = 1
FIELD_SIZE = (int(48 * k), int(27 * k))
BORDER_SIZE = 1
FPS = 10
DEBUG = False

if DEBUG:
    window = pyglet.window.Window()
else:
    window = pyglet.window.Window(fullscreen=True)


class Side(Enum):
    west = (-1, 0)
    east = (1, 0)
    north = (0, 1)
    south = (0, -1)


def get_body_parts(team):
    if team == 0:
        return painted_body_parts[0]
    elif team == 1:
        return painted_body_parts[1]
    else:
        return painted_body_parts[2]


def screen_config():
    global SCALE_X, SCALE_Y, window, BLOCK_SIZE, BORDER_SIZE
    if not DEBUG:
        window.set_exclusive_mouse()
    window.activate()
    window.switch_to()
    window.dispatch_events()
    window.dispatch_event("on_draw")
    SCALE_X = window.width / ((FIELD_SIZE[0] + 1) * BLOCK_SIZE[0])
    SCALE_Y = window.height / ((FIELD_SIZE[1] + 1) * BLOCK_SIZE[1])
    BLOCK_SIZE = BLOCK_SIZE[0] * SCALE_X, BLOCK_SIZE[1] * SCALE_Y
    BORDER_SIZE = min(BLOCK_SIZE) // 2


screen_config()
