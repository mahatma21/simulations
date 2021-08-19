import pygame
from pygame.locals import *
import random

from scripts import game_engine as ge
from scripts import entity
from scripts.constants import *


class Game:

    def __init__(self):
        pygame.init()

        entity.BgRect.set_colors(CYAN, LIGHTING_COLOR)
        self.rects = pygame.sprite.Group()
        self.rect_spawn = pygame.USEREVENT + 1
        pygame.time.set_timer(self.rect_spawn, 200)

        entity.Particle.set_colors(CYAN, LIGHTING_COLOR)
        self.particles = pygame.sprite.Group()
        self.particle_spawn = pygame.USEREVENT + 2
        pygame.time.set_timer(self.particle_spawn, 300)

        self.upper_entities = pygame.sprite.Group()
        self.upper_entity_spawn = pygame.USEREVENT + 3
        pygame.time.set_timer(self.upper_entity_spawn, 1500)

        self.clock = pygame.time.Clock()
        self.fps_counter = ge.FpsCounter(60, 10)

        self.display = pygame.display.set_mode(flags=FULLSCREEN | DOUBLEBUF)
        self.screen = pygame.Surface(SCREEN_SIZE)
        self.screen_r = self.screen.get_rect()

    def run_game(self):
        self.running = True
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.draw()
            self.draw_screen()

            self.check_events()

            self.update()

            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if ge.check_game_quit(event):
                self.running = False
            if event.type == self.rect_spawn:
                self.generate_rect()
            if event.type == self.particle_spawn:
                self.generate_particle()
            if event.type == self.upper_entity_spawn:
                self.generate_upper_entity()

    def update(self):
        self.fps_counter.get_dt()

    def generate_rect(self):
        size = random.randint(10, 100)
        entity.BgRect(
            (
                random.randint(-size, SCREEN_SIZE[0] - size),
                SCREEN_SIZE[1] + size, size, size
            ), 0, random.randint(-5, -3), random.uniform(-1, 1),
            random.randint(0, 89), random.randint(0, 10),
            self.rects
        )

    def generate_particle(self):
        particle = entity.Particle(
            random.randint(0, SCREEN_SIZE[0]), SCREEN_SIZE[1],
            0, random.randint(-3, -2), random.randint(1, 3),
            self.particles
        )
        image_rect = particle.lighting_image.get_rect(
            midtop=(particle.pos.x, SCREEN_SIZE[1]))
        particle.pos = image_rect.center

    def generate_upper_entity(self):
        upper_entity = entity.UpperEntity(
            (0, 0, 50, SCREEN_LENGTH), -3, -1.9, -45, self.upper_entities)
        upper_entity.rect.center = SCREEN_SIZE[0] + upper_entity.rect.width, SCREEN_SIZE[1] + upper_entity.rect.width

    def draw_screen(self):
        self.display.blit(self.screen, (0, 0))

        pygame.display.update()

    def draw(self):
        self.screen.fill(BG_COLOR)

        for bg_entity in self.rects:
            bg_entity.draw(self.screen)
            bg_entity.update(self.fps_counter.dt)
            self.check_border(bg_entity)

        for particle in self.particles:
            particle.draw(self.screen)
            particle.update(self.fps_counter.dt)
            self.check_border(particle)

        for upper_entity in self.upper_entities:
            upper_entity.draw(self.screen)
            upper_entity.update(self.fps_counter.dt)

            if ((not upper_entity.rect.colliderect(self.screen_r))
                    and (upper_entity.rect.centerx < 0
                         and upper_entity.rect.centery < 0)):
                upper_entity.kill()

    @staticmethod
    def check_border(obj):
        if obj.image_rect.bottom < 0:
            obj.kill()
