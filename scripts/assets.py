import pygame
import os 

W = H = 8
CANVAS_SIZE = 24
DISPLAY_SIZE = [CANVAS_SIZE * 16, CANVAS_SIZE * 30]
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
DISPLAY_COPY = pygame.Surface(DISPLAY_SIZE)

pygame.init()


# Folders
SPRITES_FOLDER = os.path.realpath(os.path.join('assets/images/sprites'))
MAPS_FOLDER = os.path.realpath(os.path.join('assets/maps'))
FONTS_FOLDER = os.path.realpath(os.path.join('assets/fonts'))
SOUNDS_FOLDER = os.path.realpath(os.path.join('assets/sounds'))


class SpriteSheet:
    def __init__(self, file_name):
        self.file = pygame.image.load(os.path.join(SPRITES_FOLDER, file_name)).convert_alpha()
        self.w = self.file.get_width()
        self.h = self.file.get_height()

    def get_sprite(self, x, y):
        sprite = pygame.Surface((W, H))
        sprite.blit(self.file, (0, 0), (x*W, y*H, W, H))
        sprite = pygame.transform.scale(sprite, [CANVAS_SIZE, CANVAS_SIZE])
        sprite.set_colorkey('black')
        return sprite

    def get_sprites(self, x_start, x_end, y_start, y_end):
        sprites = []
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                sprites.append(self.get_sprite(x, y))

        return sprites


def load_sound(sound_name):
    sound = pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, sound_name))
    sound.set_volume(.2)
    return sound


class ScreenShake:
    def __init__(self):
        self.screen_shake_time = 0
        self.earthquake_sound = load_sound('earthquake_sound.wav')

    def shake_screen(self, _time):
        self.earthquake_sound.play()
        self.screen_shake_time = _time

    def update(self):
        if self.screen_shake_time:
            self.screen_shake_time -= 1


ScreenShakeObject = ScreenShake()

# Assets
# Colors
lava_color = (229, 59, 68)
# Images
background_image = pygame.transform.scale(
    pygame.image.load(os.path.join('assets/images/backgrounds', 'background.png')).convert_alpha(), DISPLAY_SIZE)
background_image.set_alpha(95)