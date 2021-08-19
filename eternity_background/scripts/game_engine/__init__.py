import pygame
from pygame.locals import *
import sys
import os
import json
import itertools as it
import time


def get_path(*path: str):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, *path)


def get_surf(size: tuple[int]):
    surf = pygame.Surface(size)
    surf.set_colorkey('black')
    return surf


def load_image(*path: str):
    return pygame.image.load(get_path(*path))


def check_game_quit(event: int) -> bool:
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        return True
    return False


def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2,) * 2)
    surf.set_colorkey('black')
    pygame.draw.circle(surf, Color(color), (radius,) * 2, radius)
    return surf


def rect_surf(rect, color, width=0):
    surf = pygame.Surface(pygame.Vector2(rect.size) * 2)
    surf.set_colorkey('black')

    draw_rect = rect.copy()
    draw_rect.center = draw_rect.size

    pygame.draw.rect(surf, color, draw_rect, width)
    return surf


class Physics(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.movement = pygame.Vector2()
        self.momentum = pygame.Vector2()


class Entity(Physics):
    image: pygame.Surface

    def __init__(self, rect: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.rect = Rect(rect)
        self.rotation = 0
        self.air_time = 0

    def move(self, dt=1):
        self.rect.move_ip(self.movement* dt)

    def draw_rect(self, screen: pygame.Surface, color, width=0, scroll=(0, 0)):
        pygame.draw.rect(screen, Color(color), self.rect.move(scroll), width)

    def rect_surf(self, color: Color, width=0) -> pygame.Surface:
        return rect_surf(self.rect, color, width)

    @property
    def rotated_image(self):
        return pygame.transform.rotate(
            self.image, self.rotation
        )

    @classmethod
    def from_image(cls, image: pygame.Surface, *groups: pygame.sprite.Group, **pos_kwargs):
        image_rect = image.get_rect(**pos_kwargs)
        entity = cls(image_rect, *groups)
        entity.image = image
        return entity


class Particle(Physics):
    gravity: float
    radius_dec: float
    color: Color

    def __init__(self, x, y, x_vel, y_vel, radius, *groups):
        super().__init__(*groups)
        self.pos = pygame.Vector2(x, y)
        self.movement.update(x_vel, y_vel)
        self.radius = radius

    def update(self):
        self.pos += self.movement
        self.movement.y += self.gravity

        self.radius -= self.radius_dec
        if self.radius <= 0:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def get_image(self, radius=None, color=None):
        radius = radius if radius is not None else self.radius
        color = Color(color if color is not None else self.color)
        image = get_surf((radius * 2,) * 2)
        pygame.draw.circle(image, color, (radius, radius), radius)
        return image

    @classmethod
    def set(cls, gravity, radius_dec, color):
        cls.gravity = gravity
        cls.radius_dec = radius_dec
        cls.color = Color(color)


class SpriteSheet:

    def __init__(self, *sprite_sheet_path: str):
        # 'assets\spritesheet'
        self.path = get_path(*sprite_sheet_path)
        self.image = load_image(self.path + '.png').convert_alpha()

        with open(self.path + '.json') as f:
            self.data = json.load(f)

    def get_sprite(self, rect: Rect) -> pygame.Surface:
        sprite = self.image.subsurface(rect)
        return sprite

    def parse_sprite(self, name: str) -> pygame.Surface:
        sprite_data = self.data['frames'][name]['frame']
        sprite_rect = Rect(*sprite_data.values())
        sprite_image = self.get_sprite(sprite_rect)
        return sprite_image


class FpsCounter:

    def __init__(self, default_fps: int, history_length: int):
        self.default_fps = default_fps
        self.fps_data = list(it.repeat(self.default_fps, history_length))
        self.dt = 0
        self.fps = self.default_fps
        self.__last_time = 0

    def get_dt(self):
        current_time = time.time()
        dt = current_time - self.__last_time
        self.__last_time = current_time

        self.fps = 1_000 / (dt * 1_000)
        self.fps_data.pop(0)
        self.fps_data.append(self.fps)
        self.dt = self.default_fps / (sum(self.fps_data) / len(self.fps_data))

        return self.dt
