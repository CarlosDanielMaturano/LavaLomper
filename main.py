from scripts.level import *
from sys import exit

maps = [f'map_{x}.json' for x in range(1, 4)]


def main_game_loop():
    clock = pygame.time.Clock()
    index = 0
    level = Level(maps[index])
    while True:
        clock.tick(60)
        DISPLAY.fill('black')
        response = level.run()
        if response == 'reset':
            level = Level(maps[index])
        if response == 'next':
            index += 1
            if index >= len(maps):
                exit()
            level = Level(maps[index])

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == '__main__':
    main_game_loop()
