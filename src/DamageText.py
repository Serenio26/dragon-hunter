import pygame

from src.env import FONT


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = FONT.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        #morve damage text up
        self.rect.y -= 1
        #delete text
        self.counter += 1
        if self.counter > 38:
            self.kill()
