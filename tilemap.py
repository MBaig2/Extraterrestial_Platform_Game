import pygame as pg
import pytmx
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


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.tmxdata = tm
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tilewidth
        # self.tiled_objects = pytmx.TiledObject

    def render(self, surface):
        # ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile_bitmap = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile_bitmap:
                        surface.blit(
                            tile_bitmap,
                            (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight),
                        )

            elif isinstance(layer, pytmx.TiledImageLayer):
                img_bitmap = self.tmxdata.get_tile_image_by_gid(layer.gid)
                surface.blit(img_bitmap, (0, 0))

        # for layer in self.tmxdata.visible_object_groups:
        #     if isinstance(layer, pytmx.TiledObject):
        #         img_bitmap = self.tmxdata.get_tile_image_by_gid(layer.gid)
        #         surface.blit(img_bitmap, (0, 0))

        # This doesn't work but I tried to do this

        # elif isinstance(layer, pytmx.TiledObject):
        #     for x, y, gid in layer:
        #         for objects in self.tmxdata.objects:
        #             if objects.name == "Background":
        #                 img_bitmap = self.tmxdata.get_tile_image_by_gid(gid)

        #                 surface.blit(img_bitmap, (objects.x, objects.y))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def complexCamera(self, target):
        x = -target.rect.centerx + WIDTH // 2
        y = -target.rect.centery + HEIGHT // 2

        self.camera.topleft += (
            vec(x, y) - vec(self.camera.topleft)
        ) * CAMERA_SMOOTHNESS_FACTOR
        self.camera.x = max(-(self.width - WIDTH), min(0, self.camera.x))
        self.camera.y = max(-(self.height - HEIGHT), min(0, self.camera.y))


class Background(pg.sprite.Sprite):
    def __init__(self, filename, location):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.background_rate1 = 0.5
        self.background_rate2 = 0.25


class TileObjectBackground(pg.sprite.Sprite):
    def _init__(self, game, location):
        pg.sprite.Sprite.__init__(self)
