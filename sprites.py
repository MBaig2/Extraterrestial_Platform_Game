import pygame as pg
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.currentFrame = 0
        self.lastUpdate = 0
        self.load_imgs()
        self.image = self.standingFrame
        self.rect = self.image.get_rect()
        # self.rect.inflate_ip(-10, -20)
        # self.rect = pg.Rect(0, 15, 40, 60)
        # pg.draw.rect(self.image, RED, self.rect, 1)

        # Vectors
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, PLAYER_MASS * GRAVITY)

        # Charateristics of Player
        self.onGnd = True

    def load_imgs(self):
        self.standingFrame = self.game.player_graphics.get_image(24, 32, 24, 32)
        self.walkingFrames_R = [
            self.game.player_graphics.get_image(48, 32, 24, 32),
            self.game.player_graphics.get_image(0, 32, 24, 32),
        ]
        self.walkingFrames_L = []
        for frame in self.walkingFrames_R:
            self.walkingFrames_L.append(pg.transform.flip(frame, True, False))

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking and self.onGnd:
            if now - self.lastUpdate > PLAYER_ANIM_SPEED:

                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.walkingFrames_R)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walkingFrames_R[self.currentFrame]
                else:
                    self.image = self.walkingFrames_L[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_MASS * GRAVITY)
        self.move()

        # Equations of Motion
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc

        # Collision check in all 4 directions
        self.pos.x += (
            self.vel.x + 0.5 * self.acc.x * self.game.dt
        )  # Update x component (Frame-independent motion)
        if abs(self.vel.x) < PLAYER_VELX_EPSILON:
            self.vel.x = 0

        self.rect.x = self.pos.x
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:  # Horizontal collision
            if self.vel.x > 0:  # Rightward motion
                self.rect.right = hit.rect.left
            elif self.vel.y < 0:  # Leftward motion
                self.rect.left = hit.rect.right
            self.pos.x = self.rect.x  # Update true postion

        self.pos.y += self.vel.y + 0.5 * self.acc.y * self.game.dt  # Update y component
        self.rect.y = self.pos.y + 5

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
        if self.rect.bottom > HEIGHT:
            self.vel.y = 0
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.y

    def show_vectors(self):
        scale = 25
        pg.draw.line(
            self.game.screen, GREEN, self.pos, (self.pos + self.vel * scale), 5
        )


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
        image = pg.transform.scale(image, (width * 2, height * 2))
        image.set_colorkey(BLACK)
        return image


class TiledPlatform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

