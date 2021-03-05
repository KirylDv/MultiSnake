from enum import Enum
from PIL import Image
import pyglet
from helpers import replaceColor, rotate,\
                    getPygletImgFromPILImage,\
                    getAllHeadPicsFromHeadN

blueColors = [( 40,  40, 255), (  0,  38, 255), ( 62, 255,  48)] # head, sides, eyes
redColors  = [(255,  40,  40), (255,   0,  38), ( 66, 255, 214)]
# greenColors = [(40,  255,  40), (38,   255,  0), ( 200, 255, 60)]

bHeadN = Image.open("img/blue_head.png")
rHeadN = replaceColor(bHeadN, blueColors, redColors)
# gHeadN = replaceColor(bHeadN, blueColors, greenColors)

bBody = Image.open("img/blue_body.png")
rBody = replaceColor(bBody, blueColors, redColors)
# gBody = replaceColor(bBody, blueColors, greenColors)

blue_body_pic   = getPygletImgFromPILImage(bBody)
red_body_pic    = getPygletImgFromPILImage(rBody)
# green_body_pic  = getPygletImgFromPILImage(gBody)

blue_head_pics  = getAllHeadPicsFromHeadN(bHeadN)
red_head_pics   = getAllHeadPicsFromHeadN(rHeadN)
# green_head_pics = getAllHeadPicsFromHeadN(gHeadN)

apple_pic = pyglet.image.load("img/apple.png")

paintedBodyParts = [(red_body_pic, red_head_pics),
                    # (green_body_pic, green_head_pics),
                    (blue_body_pic, blue_head_pics)]

SCALE_X = 1
SCALE_Y = 1
POSSIBLE_PLAYERS = 2
PLAYERS = 2
BLOCK_SIZE = (10, 10)
k = 1
FIELD_SIZE = (int(48 * k), int(27 * k))
BORDER_SIZE = 1
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
