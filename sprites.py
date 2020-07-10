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
        self.acc = vec(0, PLAYER_MASS * GRAVITY)

        # Charateristics of Player
        self.onGnd = False

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC

    def update(self):
        self.acc = vec(0, PLAYER_MASS * GRAVITY)
        self.move()

        # Equations of Motion
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc

        # Collision check in all 4 directions
        self.pos.x += (
            self.vel.x + 0.5 * self.acc.x * self.game.dt
        )  # Update x component (Frame-independent motion)
        self.rect.x = self.pos.x
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:  # Horizontal collision
            if self.vel.x > 0:  # Rightward motion
                self.rect.right = hit.rect.left
            elif self.vel.y < 0:  # Leftward motion
                self.rect.left = hit.rect.right
            self.pos.x = self.rect.x  # Update true postion

        self.pos.y += self.vel.y + 0.5 * self.acc.y * self.game.dt  # Update y component
        self.rect.y = self.pos.y + 1

        # This prevents double jumping
        if self.vel.y > 0:
            self.onGnd = False

        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:  # Vertical Collision
            if self.vel.y > 0:  # Downward motion
                self.rect.bottom = hit.rect.top
                self.vel.y = 0
                self.onGnd = True
            elif self.vel.y < 0:  # Upward motion
                self.rect.top = hit.rect.bottom
                self.vel.y = 0
            self.pos.y = self.rect.y  # Update true postion

        # Limit Player's movement
        if self.rect.bottom >= HEIGHT:
            self.vel.y = 0
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.y


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
