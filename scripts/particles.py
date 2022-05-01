from . import * 
import random 


class LavaParticle:
    def __init__(self, pos):
        self.time = random.randint(2, 8)
        self.direction = random.choice([-1, 1])
        self.rect = pygame.Rect(pos.x, pos.y, self.time, self.time)
        self.vertical_speed = -random.randint(1, 5)
        self.horizontal_speed = random.randint(1, 5)

        self.dead = False

        self.color = lava_color

    def update(self, display):
        self.time -= .3
        if self.time <= 0:
            self.dead = True 

        self.rect.w = self.rect.h = int(self.time)

        self.rect.x += 3 * self.direction 
        self.rect.y += self.vertical_speed
        self.vertical_speed += 1

        pygame.draw.rect(display, self.color, self.rect)


class SmokeParticle:
    def __init__(self, pos):
        self.time = random.randint(1, 8)
        self.vertical_direction = random.choice([-1, 1])
        self.horizontal_direction = random.choice([-1, 1])
        self.horizontal_speed = random.randint(1, 3)/2
        self.vertical_speed = random.randint(1, 3)/2

        self.color = (175, 191, 210)

        self.pos = pygame.Vector2(pos.x, pos.y)
        self.dead = False 

    def update(self, display):
        self.time -= .3
        if self.time <= 0:
            self.dead = True 

        self.pos.x += self.horizontal_speed * self.horizontal_direction
        self.pos.y += self.vertical_speed * self.vertical_direction

        pygame.draw.circle(display, self.color, (self.pos.x, self.pos.y), self.time)        


class Particles:
    def __init__(self, display=DISPLAY_COPY):
        self.display = display
        self.particles = []

    def update(self):
        for particle in self.particles:
            if particle.dead:
                self.particles.remove(particle)
            particle.update(self.display)            

    def summon(self, pos, amount, particle):
        for x in range(amount):
            self.particles.append(particle(pos))
        

MainParticlesClass = Particles()

