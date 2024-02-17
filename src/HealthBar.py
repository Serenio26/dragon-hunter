import pygame

from src.env import RED, GREEN


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp, display):
        # update with new health
        self.hp = hp
        # cal health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(display, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(display, GREEN, (self.x, self.y, 150 * ratio, 20))
