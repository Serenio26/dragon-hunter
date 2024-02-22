import pygame

from src.env import SCREEN_HEIGHT, BOTTOM_PANEL, FONT, RED


def get_screen_mode(width: int, height: int):
    return pygame.display.set_mode((width, height))


# function for drawing img
def draw_img(img, x: int, y: int, display):
    display.blit(img, (x, y))


# function for drawing text
def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    draw_img(img=img, x=x, y=y, display=display)


# function for panel
def draw_panel(fighter, bandits: list, display):
    # panel image
    panel_img = pygame.image.load('../asset/img/Icons/panel.png').convert_alpha()
    # draw panel rectangle
    draw_img(img=panel_img, x=0, y=SCREEN_HEIGHT - BOTTOM_PANEL, display=display)
    # show knight stats
    draw_text(f'{fighter.img_folder_name} HP: {fighter.hp}', FONT, RED, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10, display)
    for count, i in enumerate(bandits):
        # show name and health
        draw_text(f'{i.img_folder_name} HP: {i.hp}', FONT, RED, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60, display)
