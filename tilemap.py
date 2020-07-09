import pygame as pg
from settings import *
from os import path

vec = pg.math.Vector2


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def complexCamera(self, target):
        x = -target.rect.centerx + WIDTH // 2
        y = -target.rect.centery + HEIGHT // 2

        self.camera.topleft += (
            vec(x, y) - vec(self.camera.topleft)
        ) * CAMERA_SMOOTHNESS_FACTOR
        self.camera.x = max(-(self.width - WIDTH), min(0, self.camera.x))
        self.camera.y = max(-(self.height - HEIGHT), min(0, self.camera.y))

