import pygame

from src.env import SCREEN, RED, GREEN


class HealthBar():
    def __init__ (self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self,hp):
        #update with new health
        self.hp = hp
        #cal health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(SCREEN, GREEN, (self.x, self.y, 150 * ratio , 20))
