import pygame
from Utility.Utils.utils import *
from Entities.MovingEntities.MovingEntity import MovingEntity
from Entities.MovingEntities.FollowBullet.FollowBullet import FollowBullet
from random import randint
from time import time
from os import path

pasta = get_folder_versao_top(__file__, 3)

class FollowBoss(MovingEntity):
    def __init__(self, game, life: int, position: tuple = None) -> None:
        self.__life = life

        self.__change_direction_time = time()
        self.__invunerable_time = time()
        self.__shot_time = time()
        self.__invunerable = False

        speed = 5
        direction = randint(0, 360)

        self.__follow_boss_invunerable_img = pygame.image.load(pasta+"//Images//follow_boss_invunerable.png")
        self.__follow_boss_img = pygame.image.load(pasta+"//Images//follow_boss.png")
        super().__init__(game, speed, -direction, self.__follow_boss_img, position)

    def hit(self) -> None:
        if (not self.invunerable):
            self.game.get_sound_mixer().play_hit_sfx()

            if (self.game.ship.invunerable):
                self.__life -= 1
            else:
                self.__life -= self.game.ship.damage

            self.__invunerable = True
            self.__invunerable_time = time()

            if (self.life <= 0):
                self.game.get_sound_mixer().play_explosion_sfx()
                self.game.get_animation_effects_manager().add_boss_explosion_effect(game=self.game,
                                                                                    position=(self.x,self.y),
                                                                                    scale=(100,100),
                                                                                    looping=False)
                self.kill()

    def set_life(self, life: int):
        self.__life = life

    def update_image_position(self) -> None:
        image = self.original_image
        self.set_image(image)
        self.set_rect(self.image.get_rect(center = (self.x, self.y)))
        self.set_mask(pygame.mask.from_surface(self.image))

    def change_direction(self) -> None:
        if ((time() - self.change_direction_time) > 3):

            direction = randint(0, 360)
            self.set_direction(direction)

            self.__change_direction_time = time()

    def check_invunerable(self) -> None:
        if (self.invunerable == True):
            if ((time() - self.__invunerable_time) > 2):
                self.__invunerable = False

    def red(self):
        img = self.__follow_boss_invunerable_img if (self.invunerable) else self.__follow_boss_img
        self.set_original_image(img)

    def shot(self):
        if ((time() - self.__shot_time) > 5):
            fb = FollowBullet(game=self.game,
                              position=(self.x,self.y),
                              direction=0,
                              speed=3,
                              damage=1,
                              lifetime=5)
            self.game.all_sprites.add(fb)
            self.game.boss_bullet_group.add(fb)
            self.game.get_sound_mixer().play_laser_shot_sfx()
            self.__shot_time = time()

    def update(self) -> None:
        self.change_direction()
        self.check_invunerable()
        self.shot()
        self.red()
        super().update()

    @property
    def invunerable(self):
        return self.__invunerable

    @property
    def invunerable_time(self):
        return self.__invunerable_time

    @property
    def change_direction_time(self):
        return self.__change_direction_time

    @property
    def life(self):
        return self.__life
