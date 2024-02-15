import pygame

from src.env import SCREEN, SCREEN_HEIGHT, BOTTOM_PANEL, FONT, RED


# panel image
panel_img = pygame.image.load('../asset/img/Icons/panel.png').convert_alpha()


# function for drawing img
def draw_img(img, x: int, y: int):
    SCREEN.blit(img, (x, y))


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    draw_img(img=img, x=x, y=y)


# function for panel
def draw_panel(fighter, bandits: list):
    # draw panel rectengale
    draw_img(img=panel_img, x=0, y=SCREEN_HEIGHT - BOTTOM_PANEL)
    # show knight stats
    draw_text(f'{fighter.name} HP: {fighter.hp}', FONT, RED, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10)
    for count, i in enumerate(bandits):
        # show name and health
        draw_text(f'{i.name} HP: {i.hp}', FONT, RED, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60)


