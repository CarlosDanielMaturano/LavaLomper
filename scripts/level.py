import json
import random
from time import sleep
from .entity import *
from .lava import *
from .player import *
from .particles import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class Level:
    def __init__(self, map_filename):
        self.map_data = []
        self.blocks_sprite_sheet = SpriteSheet('blocks.png')
        self.tiles_sprites = dict(enumerate(self.blocks_sprite_sheet.get_sprites(
            0, int(self.blocks_sprite_sheet.w/8), 0, int(self.blocks_sprite_sheet.h/8))))

        self.player_spawn = [0, 0]
        self.map_filename = map_filename
        self.load_map(map_filename)

        self.tiles_group = pygame.sprite.Group()
        self.entities_group = pygame.sprite.Group()
        self.player = Player(self.player_spawn, self.tiles_group)
        self.lava = Lava(self.player, self.entities_group)
        self.groups = [self.tiles_group, self.entities_group, self.lava, pygame.sprite.GroupSingle(self.player)]

        self.setup_level()

        self.display = pygame.display.get_surface()
        self.custom_display = DISPLAY_COPY
        self.custom_display.set_colorkey('black')
        MainParticlesClass.display = self.custom_display

        self.screen_shake_time = ScreenShakeObject.screen_shake_time
        self.render_offset = [0, 0]

    def setup_level(self):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                tile: int = tile
                pos = [x*CANVAS_SIZE, y*CANVAS_SIZE]
                if tile in self.tiles_sprites:
                    self.tiles_group.add(Tile(pos, self.tiles_sprites[tile]))
                elif tile in ENTITIES:
                    self.entities_group.add(ENTITIES[tile](self.player, pos))

    def load_map(self, map_filename):
        with open(os.path.join(MAPS_FOLDER, map_filename)) as file:
            data = json.load(file)
            self.map_data = data['tiles_data']
            self.player_spawn = data['player_spawn']

    def run(self):
        self.custom_display.fill('black')
        self.custom_display.blit(background_image, (0, 0))
        self.render_offset = [0, 0]

        [group.draw(self.custom_display) for group in self.groups]
        if not self.player.dead:
            [group.update() for group in self.groups]
            ScreenShakeObject.update()
            MainParticlesClass.update()
        else:
            if self.player.update() == 'reset':
                MainParticlesClass.particles.clear()
                self.custom_display.fill('black')
                return 'reset'
            self.render_offset = [0, 0]

        if self.player.coins == 0:
            sleep(1)
            return 'next'

        if ScreenShakeObject.screen_shake_time:
            self.render_offset = [random.randint(0, 8) - 4, random.randint(0, 8) - 4]

        self.display.blit(self.custom_display, self.render_offset)
