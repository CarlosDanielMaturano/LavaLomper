from .assets import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, tiles):
        super().__init__()
        self.sprite_sheet = SpriteSheet('lava_lomper.png')
        self.images = dict(enumerate(self.sprite_sheet.get_sprites(
            0, int(self.sprite_sheet.w/8), 0, int(self.sprite_sheet.h/8))))
        self.frame_index = 0
        self.image = self.images[self.frame_index]

        self.tiles = tiles
        self.spawn_pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.movement = pygame.Vector2(0, 0)
        self.max_vertical_speed = 15
        self.vertical_speed = self.direction = 1
        self.horizontal_speed = 3
        self.jumping = self.on_ground = False
        self.dead = False
        self.angle = 0

        self.dead_sound = load_sound('player/player_death_sound.wav')
        self.jump_sound = load_sound('player/player_jump_sound.wav')

        self.coins = 0

    def animate(self):
        self.frame_index += .15
        if not int(self.frame_index) in self.images or self.movement.x == 0:
            self.frame_index = 0

        self.image = self.images[int(self.frame_index)]
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_sound.play()
        if self.jumping:
            self.vertical_speed -= 3
        if self.vertical_speed <= -10:
            self.jumping = False

    def get_input(self):
        self.movement = pygame.Vector2(0, 1)

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.movement.x = self.direction = -1
        elif key[pygame.K_d]:
            self.movement.x = self.direction = 1
        if key[pygame.K_SPACE] and (self.on_ground or self.jumping):
            self.jump()
        else:
            self.jumping = False

    def apply_horizontal_movement(self):
        self.rect.x += self.movement.x * self.horizontal_speed

        for tile in self.tiles:
            if self.rect.colliderect(tile.rect):
                if self.movement.x > 0:
                    self.rect.right = tile.rect.left
                elif self.movement.x < 0:
                    self.rect.left = tile.rect.right
                self.frame_index = 0

    def apply_vertical_movement(self):
        self.on_ground = False
        self.movement.y = self.vertical_speed
        self.rect.y += self.movement.y
        if self.rect.y >= DISPLAY_SIZE[1]:
            self.dead = True

        for tile in self.tiles:
            if self.rect.colliderect(tile.rect):
                if self.movement.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                elif self.movement.y < 0:
                    self.rect.top = tile.rect.bottom
                self.vertical_speed = 1

        if not self.on_ground and self.vertical_speed < self.max_vertical_speed:
            self.vertical_speed += .8

    def kill(self):
        self.dead_sound.play()
        self.dead = True
        self.vertical_speed = -10

    def dead_animation(self):
        self.rect.y += self.vertical_speed
        self.vertical_speed += 1
        self.angle += 4

        self.image = pygame.transform.rotozoom(self.images[0].copy(), self.angle, 1)
        self.image.set_colorkey('black')

        if self.rect.y > DISPLAY_SIZE[1] + CANVAS_SIZE:
            return 'reset'

    def update(self):
        if self.dead:
            return self.dead_animation()
        self.get_input()
        self.animate()
        self.apply_vertical_movement()
        self.apply_horizontal_movement()
