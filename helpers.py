import heapq
from collections import namedtuple

import numpy as np
import pyglet
from PIL import Image


def replace_color(image, rgbs, new_rgbs):
    im = image.convert('RGBA')

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    # pylint: disable = unpacking-non-sequence
    red, green, blue, _ = data.T

    for i in range(len(rgbs)):

        color_areas = (red == rgbs[i][0]) & (green == rgbs[i][1]) & (blue == rgbs[i][2])
        data[..., :-1][color_areas.T] = new_rgbs[i]

    im2 = Image.fromarray(data)

    return im2


def rotate(image, action):
    return image.transpose(action)


def get_pyglet_img_from_pil_image(img):
    return pyglet.image.ImageData(img.width, img.height, 'RGBA', img.tobytes(), pitch = -img.width * 4)


def get_all_head_pics_from_head_n(head_n):
    Pics = namedtuple('Pic', ['n', 'w', 's', 'e'])

    head_w = rotate(head_n, Image.ROTATE_90)
    head_s = rotate(head_n, Image.FLIP_TOP_BOTTOM)
    head_e = rotate(head_w, Image.FLIP_LEFT_RIGHT)

    return Pics(n=get_pyglet_img_from_pil_image(head_n),
                w=get_pyglet_img_from_pil_image(head_w),
                s=get_pyglet_img_from_pil_image(head_s),
                e=get_pyglet_img_from_pil_image(head_e))


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def push(self, key, item):
        heapq.heappush(self.elements, (key, item))

    def pop(self):
        return heapq.heappop(self.elements)
