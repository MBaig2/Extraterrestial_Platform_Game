import pygame as pg
import pytmx
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
        game_folder = path.dirname(__file__)
        image_dir = path.join(game_folder, "Imgs")
        map_dir = path.join(game_folder, "maps")
        self.map = TiledMap(path.join(map_dir, "Map1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # Load player graphics
        self.player_graphics = SpriteSheet(path.join(image_dir, PLAYER_SPRITESHEET))
        self.platform_graphics = SpriteSheet(
            path.join(image_dir, "tileset1_padded.png")
        )
        self.background = Background(path.join(image_dir, "rock.png"), [0, 0])

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Platform(self, col, row)
        #         if tile == "p":
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "Player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "Platform":
                TiledPlatform(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
            if tile_object.name == "Background":
                self.img_bitmap = self.map.tmxdata.get_tile_image_by_gid(
                    tile_object.gid
                )

                self.temp_rect = pg.Rect(0, 0, tile_object.width, tile_object.height)
        self.camera = Camera(self.background.rect.width, self.background.rect.height)
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
        self.camera.complexCamera(self.background)
        self.camera.complexCamera(self.player)

    def events(self):
        # Game Loop - eventsddd
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.player.onGnd:
                    self.player.vel.y = PLAYER_JUMP
                    self.player.pos.y -= 20
                    self.player.onGnd = False

                self.running = False

    def draw(self):
        # Game Loop - draw
        self.font = pg.font.Font(None, 30)
        self.screen.fill(WHITE)
        # Track Background for parallax effect
        self.screen.blit(
            self.background.image, self.camera.apply_rect(self.background.rect)
        )
        # self.screen.blit(self.backimg, (0, 0))

        self.screen.blit(self.img_bitmap, self.camera.apply_rect(self.temp_rect))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            self.fps = self.font.render(
                str(int(self.clock.get_fps())), True, pg.Color("gray11")
            )
            # self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
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
