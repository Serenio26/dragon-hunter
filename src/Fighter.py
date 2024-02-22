import random

import pygame

from src.DamageText import DamageText
from src.env import RED, DAMAGE_TEXT_GROUP, KNIGHT, BANDIT


class Fighter():
    def __init__(self, x: int, y: int, img_folder_name: str, max_hp: int, strength: int, potions: int):
        self.img_folder_name = img_folder_name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'../asset/img/{self.img_folder_name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'../asset/img/{self.img_folder_name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'../asset/img/{self.img_folder_name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'../asset/img/{self.img_folder_name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    # update image
    def update(self):
        # handle information
        self.image = self.animation_list[self.action][self.frame_index]
        animation_cooldown = 100
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the imformation has run out then back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # set variables to idle action
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Deal damage to enemy
        rand = random.randint(-5, 5)
        damage = abs(self.strength + rand)
        target.hp -= damage
        # run enemy hurt animetion
        target.hurt()
        # check if target died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), RED)
        DAMAGE_TEXT_GROUP.add(damage_text)
        # set variables to attack action
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variables to hurt action
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variables to hurt action
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self, is_win=False):
        if is_win:
            if self.img_folder_name == KNIGHT:
                self.max_hp += random.randint(5, 16)
                self.strength += random.randint(1, 11)
                self.potions += random.randint(1, 3)

            elif self.img_folder_name == BANDIT:
                self.max_hp += 10
                self.strength += 5
                self.potions += 1

        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    # draw image
    def draw(self, display):
        display.blit(self.image, self.rect)
