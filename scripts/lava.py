from .assets import *
from .particles import *
from random import randint


class LavaTile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.sprite_sheet = SpriteSheet('lava.png')
        self.sprites = self.sprite_sheet.get_sprites(0, int(self.sprite_sheet.w/8), 0, int(self.sprite_sheet.h/8))
        self.frame_index = randint(0, len(self.sprites) - 1)
        self.image = self.sprites[self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):
        self.frame_index += .15
        if self.frame_index >= len(self.sprites):
            self.frame_index = 0
        self.image = self.sprites[int(self.frame_index)]

    def update(self, y):
        if randint(0, 100) == 35:
            MainParticlesClass.summon(self.rect, 15, LavaParticle)
        self.rect.y = y
        self.animate()


class Lava:
    def __init__(self, player, entities_group):
        self.image = pygame.Surface(DISPLAY_SIZE)
        self.image.fill(lava_color)
        self.lava_tiles = pygame.sprite.Group()

        self.alpha = 0
        self.red_surface = pygame.Surface(DISPLAY_SIZE)
        self.red_surface.fill('red')

        self.kill_rect = pygame.Rect(0, DISPLAY_SIZE[1] + 100, 30 * CANVAS_SIZE, CANVAS_SIZE)
        for x in range(30):
            self.lava_tiles.add(LavaTile([x*CANVAS_SIZE, self.kill_rect.y]))

        self.speed = 0.1
        self.player = player
        self.entities_group = entities_group

    def draw(self, display):
        display.blit(self.red_surface, (0, 0))
        self.lava_tiles.draw(display)
        self.lava_tiles.update(self.kill_rect.y-10)
        display.blit(self.image, self.kill_rect)

    def update(self):
        if randint(0, 300) == 100:
            ScreenShakeObject.shake_screen(30)
        self.alpha += .1
        self.red_surface.set_alpha(self.alpha)
        self.kill_rect.y -= self.speed
        if self.kill_rect.colliderect(self.player.rect):
            self.player.kill()

        for entity in self.entities_group:
            if self.kill_rect.colliderect(entity):
                entity.kill()