import pygame as pg
from sprites import *
from settings import *
from tilemap import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True

    def load_data(self):
        self.dir = path.dirname(__file__)
        image_dir = path.join(self.dir, "Imgs")
        self.map = Map(path.join(self.dir, "map1.txt"))
        # Load player graphics
        self.player_graphics = SpriteSheet(path.join(image_dir, PLAYER_SPRITESHEET))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Platform(self, col, row)
                if tile == "p":
                    self.player = Player(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000  # Convert ms to seconds
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.complexCamera(self.player)

        # Collide only if players are falling. Will need to change when I implement different types of platforms
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if self.player.vel.y > 0:
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:

                    self.player.jump()

                self.running = False

    def draw(self):
        # Game Loop - draw
        self.font = pg.font.Font(None, 30)
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.fps = self.font.render(
                str(int(self.clock.get_fps())), True, pg.Color("white")
            )
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            # Blit FPS for debugging purposes only. Remove in future release
            self.screen.blit(self.fps, (50, 50))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


if __name__ == "__main__":
    Game().new()
    pg.quit()
