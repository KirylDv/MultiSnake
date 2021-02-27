from collections import namedtuple
from enum import Enum

import pyglet

Pics = namedtuple('Pic', ['w', 'n', 's', 'e'])

blue_body_pic = pyglet.image.load("img/blue_body.png")
red_body_pic = pyglet.image.load("img/red_body.png")
blue_head_pics = Pics(w=pyglet.image.load("img/blue_head_w.png"),
                      n=pyglet.image.load("img/blue_head_n.png"),
                      e=pyglet.image.load("img/blue_head_e.png"),
                      s=pyglet.image.load("img/blue_head_s.png"))
red_head_pics = Pics(w=pyglet.image.load("img/red_head_w.png"),
                     n=pyglet.image.load("img/red_head_n.png"),
                     e=pyglet.image.load("img/red_head_e.png"),
                     s=pyglet.image.load("img/red_head_s.png"))
apple_pic = pyglet.image.load("img/apple.png")

SCALE_X = 1
SCALE_Y = 1
POSSIBLE_PLAYERS = 2
PLAYERS = 2
BLOCK_SIZE = (10, 10)
k = 1
FIELD_SIZE = (int(48 * k), int(27 * k))
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


def screen_config():
    global SCALE_X, SCALE_Y, window, BLOCK_SIZE
    if not DEBUG:
        window.set_exclusive_mouse()
    window.activate()
    window.switch_to()
    window.dispatch_events()
    window.dispatch_event("on_draw")
    SCALE_X = window.width / ((FIELD_SIZE[0] + 1) * BLOCK_SIZE[0])
    SCALE_Y = window.height / ((FIELD_SIZE[1] + 1) * BLOCK_SIZE[1])
    BLOCK_SIZE = BLOCK_SIZE[0] * SCALE_X, BLOCK_SIZE[1] * SCALE_Y


screen_config()
