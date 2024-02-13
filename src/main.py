import pygame

from src.Button import Button
from src.DamageText import DamageText
from src.Fighter import Fighter
from src.HealthBar import HealthBar
from src.env import RED, GREEN, SCREEN, SCREEN_HEIGHT, BOTTOM_PANEL, DAMAGE_TEXT_GROUP, FONT

# pygame.init()

# set Frame rate
clock = pygame.time.Clock()
fps = 60

# game window

# to run window
pygame.display.set_caption('Battle screen')

# define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 10
clicked = False
game_over = 0

# load image
# backgroud images
background_img = pygame.image.load('../asset/img/Background/background.png').convert_alpha()
# panel image
panel_img = pygame.image.load('../asset/img/Icons/panel.png').convert_alpha()
# buttom image
potion_img = pygame.image.load('../asset/img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('../asset/img/Icons/restart.png').convert_alpha()
# load victory and defeat image
victory_img = pygame.image.load('../asset/img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('../asset/img/Icons/defeat.png').convert_alpha()
# sword image
sword_img = pygame.image.load('../asset/img/Icons/sword.png').convert_alpha()


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x, y))


# function for drawing background
def draw_bg():
    SCREEN.blit(background_img, (0, 0))


# function for panel
def draw_panel():
    # draw panel rectengale
    SCREEN.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))
    # show knight stats
    draw_text(f'{knight.name} HP: {knight.hp}', FONT, RED, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10)
    for count, i in enumerate(bandit_list):
        # show name and health
        draw_text(f'{i.name} HP: {i.hp}', FONT, RED, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60)


# fighter class


knight = Fighter(200, 260, 'Knight', 50, 10, 3)
bandit1 = Fighter(550, 260, 'Bandit', 10, 6, 1)
bandit2 = Fighter(700, 260, 'Bandit', 10, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 100, bandit2.hp, bandit2.max_hp)

# button class

# create button
potion_button = Button(SCREEN, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 70, potion_img, 64, 64)
restart_button = Button(SCREEN, 330, 120, restart_img, 120, 30)

# main game runnign system
run = True
while run:
    clock.tick(fps)

    # draw background
    draw_bg()

    # draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    # draw fighter
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    # draw damage text
    DAMAGE_TEXT_GROUP.update()
    DAMAGE_TEXT_GROUP.draw(SCREEN)

    # control player action
    # resert action variables
    attack = False
    potion = False
    target = None
    # make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            # hide mouse
            pygame.mouse.set_visible(False)
            # show sowrd in place of mouse cursor
            SCREEN.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:
                attack = True
                target = bandit_list[count]
    if potion_button.draw():
        potion = True
    # show how many left
    draw_text(str(knight.potions), FONT, RED, 150, SCREEN_HEIGHT - BOTTOM_PANEL + 70)

    if game_over == 0:
        # player action
        if knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # look for player action
                    # attack
                    if attack == True and target != None:
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    # potion
                    if potion == True:
                        if knight.potions > 0:
                            # check if potion will heal player beond mx health
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), GREEN)
                            DAMAGE_TEXT_GROUP.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        # enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # check if bandit need to heal first
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), GREEN)
                            DAMAGE_TEXT_GROUP.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        # attack
                        else:
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        # if all fighter have turn then reset
        if current_fighter > total_fighters:
            current_fighter = 1

    # check if all bandit are dead
    alive_bandit = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandit += 1
    if alive_bandit == 0:
        game_over = 1

    # check if game is over
    if game_over != 0:
        if game_over == 1:
            SCREEN.blit(victory_img, (250, 50))
        if game_over == -1:
            SCREEN.blit(defeat_img, (250, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
