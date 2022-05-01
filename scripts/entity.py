from .assets import *
from .particles import *
from random import randint, choice


class Entity(pygame.sprite.Sprite):
    def __init__(self, player, pos, sprite_sheet_filename, animation_speed, variations=True):
        super().__init__()
        self.sprite_sheet = SpriteSheet(sprite_sheet_filename)
        self.sprites = self.sprite_sheet.get_sprites(0, int(self.sprite_sheet.w/8), 0, int(self.sprite_sheet.h/8))

        if variations:
            # if the entity has variations, get only the sprites of one random variation
            w = int((self.sprite_sheet.w/8))
            h = int(self.sprite_sheet.h/8)
            self.variation = randint(0, int((len(self.sprites) - 1)/h))
            self.sprites = self.sprites[self.variation*w:(self.variation + 1)*w]

        self.frame_index = 0
        self.image = self.sprites[self.frame_index]
        self.animation_speed = animation_speed
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = 1

        self.player = player

        self.destroyed_sound = load_sound('destroyed_sound.wav')

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.sprites):
            self.frame_index = 0
        self.image = self.sprites[int(self.frame_index)]
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def kill(self):
        MainParticlesClass.summon(self.rect, 10, SmokeParticle)
        self.destroyed_sound.play()
        return super().kill()

    def update(self):
        self.animate()


class Coin(Entity):
    def __init__(self, player, pos):
        super().__init__(player, pos, 'coin.png', .15, False)
        self.collected_sound = load_sound('coin_sound.wav')
        self.player.coins += 1

    def update(self):
        if self.player.rect.colliderect(self.rect):
            self.collected_sound.play()
            self.remove(self.groups()[0])
            self.player.coins -= 1
        return super().update()


class CoolBat(Entity):
    def __init__(self, player, pos):
        super().__init__(player, pos, 'cool_bat.png', .10)
        self.direction = choice([-1, 1])
        self.movement_speed = int((self.variation + 2)/2)

    def update(self):
        self.rect.x += self.movement_speed * self.direction
        for tile in self.player.tiles:
            if self.rect.colliderect(tile):
                self.direction *= -1
                break
        if self.rect.colliderect(self.player.rect):
            self.player.kill()

        return super().update()


class SpookySkeleton(Entity):
    def __init__(self, player, pos):
        super().__init__(player, pos, 'spooky_skeleton.png', .15)
        self.direction = 1 if self.player.rect.x - self.rect.x > 0 else -1
        self.movement = pygame.Vector2(0, 1)
        self.vision_radius = [CANVAS_SIZE*7, CANVAS_SIZE*(self.variation + 1)]
        self.on_ground = False

    def apply_horizontal_movement(self):
        self.rect.x += self.movement.x
        for tile in self.player.tiles:
            if self.rect.colliderect(tile):
                if self.movement.x > 0:
                    self.rect.right = tile.rect.left
                elif self.movement.x < 0:
                    self.rect.left = tile.rect.right
                self.frame_index = 0

    def apply_vertical_movement(self):
        self.on_ground = False
        self.rect.y += self.movement.y
        for tile in self.player.tiles:
            if self.rect.colliderect(tile.rect):
                if self.movement.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                elif self.movement.y < 0:
                    self.rect.top = tile.rect.bottom

        if not self.on_ground:
            self.movement.y += .5
        else:
            self.movement.y = 0

    def interact_with_player(self):
        x_distance = (self.player.rect.x - self.rect.x)
        y_distance = (self.rect.y - self.player.rect.y)

        if abs(x_distance) <= self.vision_radius[0] and abs(y_distance) <= self.vision_radius[1] \
                and not abs(x_distance) < 15:
            if x_distance < 0:
                self.direction = -1
            else:
                self.direction = 1
            self.movement.x = 2*self.direction
        else:
            self.movement.x = 0

        if self.rect.colliderect(self.player.rect):
            self.player.kill()

    def animate(self):
        if self.movement.x == 0:
            self.image = self.sprites[0] if self.direction == 1 else pygame.transform.flip(self.sprites[0], True, False)
            return
        return super().animate()

    def update(self):
        self.interact_with_player()
        self.apply_vertical_movement()
        self.apply_horizontal_movement()
        self.animate()


ENTITIES = {
    4: Coin,
    6: SpookySkeleton,
    7: CoolBat
}
