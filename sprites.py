import pygame as pg
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.player_graphics.get_image(48, 0, 48, 56)
        self.rect = self.image.get_rect()

        # Vectors
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # Charateristics of Player
        self.onGnd = False
        self.jumpStrength = PLAYER_JUMP

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x += -1
        if hits:
            self.vel.y = PLAYER_JUMP

    def get_keys(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC

        # Equations of Motion
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc * self.game.dt  # Frame-independent motion

        # Limit Player's movement
        if self.pos.x > self.game.map.width:
            self.pos.x = self.game.map.width
        if self.pos.x < 0:
            self.pos.x = 0

    def update(self):
        self.get_keys()
        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class SpriteSheet:
    """ Class to load and parse a spritesheet

        x = Top Left x coordinate (in pixels)
        y = Top Left y coordinate (in pixels)
        width = width of desired cutout rectangle (in pixels)
        height = height of desired cutout rectangle (in pixels)
    """

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Will 'cut' desired sprite out of a larger image sheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image
