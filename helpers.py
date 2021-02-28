from collections import namedtuple
from PIL import Image
import numpy as np
import pyglet

def replaceColor (image, rgbs, newRgbs):
    im = image.convert('RGBA')

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    # pylint: disable = unpacking-non-sequence
    red, green, blue, _ = data.T

    for i in range(len(rgbs)):

        color_areas = (red == rgbs[i][0]) & (green == rgbs[i][1]) & (blue == rgbs[i][2])
        data[..., :-1][color_areas.T] = newRgbs[i]

    im2 = Image.fromarray(data)

    return im2

def rotate(image, action):
    return image.transpose(action)

def getPygletImgFromPILImage(img):
    return pyglet.image.ImageData(img.width, img.height, 'RGBA', img.tobytes(), pitch = -img.width * 4)

def getAllHeadPicsFromHeadN(headN):
    Pics = namedtuple('Pic', ['n', 'w', 's', 'e'])

    headW = rotate(headN, Image.ROTATE_90)
    headS = rotate(headN, Image.FLIP_TOP_BOTTOM)
    headE = rotate(headW, Image.FLIP_LEFT_RIGHT)

    return Pics(n = getPygletImgFromPILImage(headN),
                w = getPygletImgFromPILImage(headW),
                s = getPygletImgFromPILImage(headS),
                e = getPygletImgFromPILImage(headE))
