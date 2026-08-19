import pygame as pg
import sys
import os
pg.init()


def load_img(path, size=None):
    if path and os.path.exists(path):
        img = pg.image.load(path).convert_alpha()
        if size:
            img = pg.transform.scale(img, size)
        return img
    return None