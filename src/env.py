import pygame

pygame.init()

# define color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SCREEN_WIDTH = 800
BOTTOM_PANEL = 150
SCREEN_HEIGHT = 400 + BOTTOM_PANEL

HOME_SCREEN_WIDTH = 800
HOME_SCREEN_HEIGHT = 530

DAMAGE_TEXT_GROUP = pygame.sprite.Group()

# define fonts
FONT = pygame.font.SysFont('Times New Roman', 26)
