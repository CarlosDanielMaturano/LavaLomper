from scripts import *
import json
import jsbeautifier


class TileImage(pygame.sprite.Sprite):
    def __init__(self, pos, image, type=0):
        super().__init__()
        self.image = pygame.transform.scale(image, [CANVAS_SIZE, CANVAS_SIZE])
        self.rect = self.image.get_rect(topleft=pos)
        self.type = type

    def draw(self, display):
        display.blit(self.image, self.rect)


class TiledMap:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.map_width = 16
        self.map_height = 30
        self.tiles_image = []
        self.fill_array()

        self.sprite_type = 0
        self.sprite_sheet = SpriteSheet('sprite_sheet.png')

        self.file_w = int(self.sprite_sheet.w / W)
        self.file_h = int(self.sprite_sheet.h / H)

        self.sprites_image = pygame.transform.scale(self.sprite_sheet.file,
                                                    [8 * int(48 / self.file_h), 8 * int(48 / self.file_w)])
        self.sprites = self.sprite_sheet.get_sprites(0, self.file_w, 0, self.file_h)

        self.information = {
            'tile_id': 0,
            'pos': [0, 0]
        }

        self.font = pygame.font.Font(os.path.join(FONTS_FOLDER, 'terminal.otf'), 28)
        self.rect = pygame.Rect(DISPLAY_SIZE[0], 0, 48, 48)
        self.grid_surface = pygame.Surface([DISPLAY_SIZE[0], DISPLAY_SIZE[1]])
        self.grid_surface.fill('white')

        try:
            self.load()
        except FileNotFoundError:
            print("Failed to open 'map.json',creating new file.")
            file = open('map.json', 'w+')
            file.close()

    def fill_array(self):
        for y in range(self.map_height):
            array_data = []
            for x in range(self.map_width):
                array_data.append(-1)
            self.tiles_image.append(array_data)

    # Get the input of adding/removing tiles and set the type of tile
    def get_input(self):

        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(0, 0, CANVAS_SIZE, CANVAS_SIZE)
        mouse_rect.center = mouse_pos
        mouse_buttons = pygame.mouse.get_pressed()

        for y in range(self.map_height):
            for x in range(self.map_width):
                pos = [x * CANVAS_SIZE, y * CANVAS_SIZE]
                if mouse_rect.collidepoint(pos):
                    self.information['pos'] = pos
                    tile = self.tiles_image[y][x]
                    if isinstance(tile, TileImage):
                        self.information['tile_id'] = tile.type
                    else:
                        self.information['tile_id'] = self.tiles_image[y][x]

                    if mouse_buttons[0]:
                        self.tiles_image[y][x] = TileImage(pos, self.sprites[self.sprite_type], self.sprite_type)
                    elif mouse_buttons[2]:
                        self.tiles_image[y][x] = -1
                        return
                    self.display.blit(self.sprites[self.sprite_type], pos)

        for y in range(self.file_h):
            for x in range(self.file_w):
                rect = pygame.Rect(DISPLAY_SIZE[0] + x * 48, y * 48, 48, 48)
                if rect.colliderect(mouse_rect):
                    if mouse_buttons[0]:
                        self.rect = rect
                        x_pos, y_pos = int(self.rect.x - DISPLAY_SIZE[0]) / 48, int(self.rect.y / 48)
                        self.sprite_type = int(y_pos * 4 + x_pos)

        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            self.fill_array()
        elif key[pygame.K_s]:
            self.save()
        elif key[pygame.K_l]:
            self.load()

    def draw_grid(self):
        self.display.blit(self.grid_surface, (0, 0))

        for y in range(self.map_height):
            for x in range(self.map_width):
                surface = pygame.Surface([CANVAS_SIZE - 1, CANVAS_SIZE - 1])
                surface.fill('black')
                self.display.blit(surface, (x * CANVAS_SIZE, y * CANVAS_SIZE))

        for y in range(self.file_h):
            for x in range(self.file_h):
                surface = pygame.Surface([48 - 1, 48 - 1])
                surface.fill('white')
                self.display.blit(surface, (DISPLAY_SIZE[0] + x * 48, y * 48))

    # Draw the tiles and information  
    def draw(self):
        for row in self.tiles_image:
            for tile in row:
                if isinstance(tile, TileImage):
                    tile.draw(self.display)

        x_pos = DISPLAY_SIZE[0] + 48 * 4
        self.display.blit(self.sprites_image, (self.map_width * CANVAS_SIZE, 0))
        self.display.blit(self.font.render(f"tile id: {self.information['tile_id']}", True, 'white'), [x_pos, 0])
        self.display.blit(
            self.font.render(f"x:{self.information['pos'][0]}, y:{self.information['pos'][1]}", True, 'white'),
            [x_pos, 32])
        self.display.blit(self.font.render(f"Sel.tile: {self.sprite_type}", True, 'white'), [x_pos, 66])
        pygame.draw.rect(self.display, 'red', self.rect, width=3)

    def update(self):
        self.draw_grid()
        self.draw()
        self.get_input()

    def save(self):
        tiles_data = []
        for y, row in enumerate(self.tiles_image):
            array_data = []
            for x, tile in enumerate(row):
                array_data.append(tile.type if isinstance(tile, TileImage) else tile)
            tiles_data.append(array_data)

        data = {'tiles_data': tiles_data, 'player_spawn': [0, 0]}
        for y, row in enumerate(tiles_data):
            for x, tile in enumerate(row):
                if tile == 5:
                    data['player_spawn'] = [x*CANVAS_SIZE, y*CANVAS_SIZE]

        options = jsbeautifier.default_options().indent_size = 2
        with open(os.path.join(MAPS_FOLDER, 'map.json'), 'w+') as file:
            file.write(jsbeautifier.beautify(json.dumps(data), options))

    def load(self, filename='map.json'):
        with open(os.path.join(MAPS_FOLDER, filename), 'r+') as file:
            map_data = json.load(file)

        for y, row in enumerate(map_data['tiles_data']):
            for x, tile in enumerate(row):
                tile = int(tile)
                pos = [x * CANVAS_SIZE, y * CANVAS_SIZE]
                self.tiles_image[y][x] = TileImage(pos, self.sprites[tile], tile) if tile != -1 else tile


def main_loop():
    pygame.display.set_mode([DISPLAY_SIZE[0] + 48 * 8, DISPLAY_SIZE[1]])
    tiled_map = TiledMap()
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        DISPLAY.fill('black')
        tiled_map.update()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


main_loop()
