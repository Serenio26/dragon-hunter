import pygame

from src.Button import Button
from src.DamageText import DamageText
from src.Fighter import Fighter
from src.HealthBar import HealthBar
from src.env import RED, GREEN, SCREEN_HEIGHT, BOTTOM_PANEL, DAMAGE_TEXT_GROUP, FONT, SCREEN_WIDTH, \
    HOME_SCREEN_WIDTH, HOME_SCREEN_HEIGHT
from src.module import draw_text, draw_img, draw_panel, get_screen_mode

# control variable
is_start = False
is_pause = False

# set Frame rate
clock = pygame.time.Clock()
fps = 60

# to run window
pygame.display.set_caption('Battle screen')
SCREEN = get_screen_mode(width=HOME_SCREEN_WIDTH, height=HOME_SCREEN_HEIGHT)

# define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
is_attack = False
potion = False
potion_effect = 10
clicked = False
game_over = 0

# load image
# main pages images
main_page_img = pygame.image.load('../asset/img/Background/main_page_img.png').convert_alpha()
# backgroud images
background_img = pygame.image.load('../asset/img/Background/background.png').convert_alpha()
menu_img = pygame.image.load('../asset/img/Background/menu_background.png').convert_alpha()
# button image
potion_img = pygame.image.load('../asset/img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('../asset/img/Icons/restart.png').convert_alpha()
start_button_img = pygame.image.load('../asset/img/Icons/start_button.png').convert_alpha()
workshop_img = pygame.image.load('../asset/img/Icons/workshop.png').convert_alpha()
# TODO 修改裝備按鈕
menu_btn_img = pygame.image.load('../asset/img/Icons/start_button.png').convert_alpha()
# load victory and defeat image
victory_img = pygame.image.load('../asset/img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('../asset/img/Icons/defeat.png').convert_alpha()
# sword image
sword_img = pygame.image.load('../asset/img/Icons/sword.png').convert_alpha()

# fighter class
knight = Fighter(200, 260, 'Knight', 50, 1, 3)
bandit1 = Fighter(550, 260, 'Bandit', 10, 10, 1)
bandit2 = Fighter(700, 260, 'Bandit', 10, 10, 1)

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

# main game running system
run = True
while run:
    clock.tick(fps)

    # draw main page
    draw_img(img=main_page_img, x=0, y=0, display=SCREEN)
    draw_img(img=start_button_img, x=HOME_SCREEN_WIDTH / 2 - 15, y=HOME_SCREEN_HEIGHT - 150, display=SCREEN)
    draw_img(img=menu_btn_img, x=10, y=10, display=SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # is_start = True
            clicked = True
        else:
            clicked = False

    # handle start btn event
    if clicked:
        start_button = Button(SCREEN, HOME_SCREEN_WIDTH / 2 - 15, HOME_SCREEN_HEIGHT - 150, start_button_img, 150, 49)
        if start_button.draw() and start_button.is_start is False:
            is_start = True
            start_button.is_start = True
            SCREEN = get_screen_mode(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

        # handle menu btn event
        menu_btn = Button(SCREEN, 10,10, menu_btn_img, 150, 49)
        if menu_btn.draw() and is_pause is False:
            is_start = False
            is_pause = True
            SCREEN = get_screen_mode(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)


    # TODO Extract Function
    if is_start:
        # draw background
        draw_img(img=background_img, x=0, y=0, display=SCREEN)

        # draw panel
        draw_panel(fighter=knight, bandits=bandit_list, display=SCREEN)
        knight_health_bar.draw(knight.hp, SCREEN)
        bandit1_health_bar.draw(bandit1.hp, SCREEN)
        bandit2_health_bar.draw(bandit2.hp, SCREEN)

        # draw fighter
        knight.update()
        knight.draw(display=SCREEN)
        for bandit in bandit_list:
            bandit.update()
            bandit.draw(display=SCREEN)

        # draw damage text
        DAMAGE_TEXT_GROUP.update()
        DAMAGE_TEXT_GROUP.draw(SCREEN)

        # control player action
        # reset action variables
        is_attack = False
        potion = False
        target = None
        # make sure mouse is visible
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                draw_img(sword_img, *pos, SCREEN)
                if clicked and bandit.alive:
                    is_attack = True

                    target = bandit_list[count]
        if potion_button.draw():
            potion = True
        # show how many left
        draw_text(str(knight.potions), FONT, RED, 150, SCREEN_HEIGHT - BOTTOM_PANEL + 70, SCREEN)

        # TODO refactor
        if game_over == 0:
            # player action
            if knight.alive:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # look for player action
                        # attack
                        if is_attack and target is not None:
                            knight.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                        # potion
                        if potion:
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
                    if bandit.alive:
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
            if bandit.alive:
                alive_bandit += 1
        if alive_bandit == 0:
            game_over = 1

        # check if game is over
        if game_over != 0:
            if game_over == 1:
                draw_img(img=victory_img, x=250, y=50, display=SCREEN)
            if game_over == -1:
                draw_img(img=defeat_img, x=250, y=50, display=SCREEN)
            if restart_button.draw():
                knight.reset()
                for bandit in bandit_list:
                    bandit.reset()
                current_fighter = 1
                action_cooldown = 0
                game_over = 0

    # TODO if xxx=True then 顯示個人資料+裝備的畫面
    if is_pause:
        draw_img(img=menu_img, x=0, y=0, display=SCREEN)
        menu_knight = Fighter(x=SCREEN_WIDTH-100, y=SCREEN_HEIGHT-100, img_folder_name="menu_knight"
                              , max_hp= 100, strength=1, potions=0)
        menu_knight.draw(display=SCREEN)
        menu_knight.update()


    pygame.display.update()

pygame.quit()
