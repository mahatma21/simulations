import pygame
from pygame.locals import *
from scripts import game_engine as ge


class UpperEntity(ge.Entity):
    color = (5, 10, 20)

    def __init__(self, rect, x_vel, y_vel, rotation, *groups):
        super().__init__(rect, *groups)
        self.movement.update(x_vel, y_vel)
        self.image = pygame.transform.rotate(self.rect_surf(self.color), rotation)

    def update(self, dt=1):
        self.move(dt)

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.rect.center))


class BgRect(ge.Entity):
    color: Color
    lighting_color: Color

    def __init__(self, rect, x_vel, y_vel, rotation_vel, rotation, width=0, *groups):
        super().__init__(rect, *groups)
        self.vel = pygame.Vector3(x_vel, y_vel, rotation_vel)
        self.rotation = rotation
        self.width = width
        self.image = self.rect_surf(self.color, self.width)
        self.lighting_image = self.rect_surf(
            self.lighting_color, (self.width if self.width > 0 else 7) * 3
        )

    def update(self, dt=1):
        vel = self.vel * dt
        self.rect.move_ip(vel[:2])
        self.rotation += vel.z

    def draw_lighting(self, screen):
        image = self.rotated_lighting_image
        screen.blit(
            image, image.get_rect(center=self.rect.center), 
            special_flags=BLEND_RGB_ADD
        )

    def draw_image(self, screen):
        image = self.rotated_image
        screen.blit(image, image.get_rect(center=self.rect.center))

    def draw(self, screen: pygame.Surface):
        self.draw_lighting(screen)
        self.draw_image(screen)

    @classmethod
    def set_colors(cls, color, lighting_color):
        cls.color = Color(color)
        cls.lighting_color = Color(lighting_color)

    @property
    def image_rect(self):
        return self.lighting_image.get_rect(center=self.rect.center)

    @property
    def rotated_lighting_image(self):
        return pygame.transform.rotate(
            self.lighting_image, self.rotation
        )


class Particle(ge.Particle):

    def __init__(self, x, y, x_vel, y_vel, radius, *groups):
        super().__init__(x, y, x_vel, y_vel, radius, *groups)
        self.image = self.get_image()
        self.lighting_image = self.get_image(self.radius * 3, self.lighting_color)

    def update(self, dt=1):
        self.pos += self.movement * dt

    def draw_lighting(self, screen):
        screen.blit(
            self.lighting_image, self.lighting_image.get_rect(center=self.pos), 
            special_flags=BLEND_RGB_ADD
        )

    def draw_image(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.pos))

    def draw(self, screen):
        self.draw_lighting(screen)
        self.draw_image(screen)

    @classmethod
    def set_colors(cls, color, lighting_color):
        cls.color = color
        cls.lighting_color = lighting_color

    @property
    def image_rect(self):
        return self.lighting_image.get_rect(center=self.pos)