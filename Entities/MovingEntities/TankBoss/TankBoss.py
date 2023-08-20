import pygame
from Utility.Utils.utils import *
from Entities.MovingEntities.MovingEntity import MovingEntity
from random import randint
from time import time
from os import path
from math import atan2, pi

pasta = get_folder_versao_top(__file__, 3)

class TankBoss(MovingEntity):
    def __init__(self, game, life: int, position: tuple = None) -> None:
        self.__life = life

        self.__change_direction_time = time()
        self.__rush_time = time()
        self.__stop_time = time()
        self.__invunerable_time = time()
        self.__invunerable = False
        self.__stop = False
        self.__activate_rush = False

        self.__rush_sound_time = 0


        speed = 5
        direction = randint(0, 360)

        self.__tank_boss_rush_img = pygame.image.load(pasta+"//Images//TankBoss_rush.png")
        self.__tank_boss_img = pygame.image.load(pasta+"//Images//TankBoss.png")
        super().__init__(game, speed, -direction, self.__tank_boss_img, position)

    def hit(self) -> None:
        if ((not self.activate_rush) and (not self.invunerable)):
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
        if (self.activate_rush == False):
            if ((time() - self.change_direction_time) > 3):

                direction = randint(0, 360)
                self.set_speed(5)
                self.set_direction(direction)

                self.__change_direction_time = time()

    def check_invunerable(self) -> None:
        if (self.invunerable == True):
            if ((time() - self.invunerable_time) > 2):
                self.__invunerable = False

    def rush(self) -> None:
        if (self.activate_rush == False):
            if ((time() - self.rush_time) > 8):
                self.__activate_rush = True
                self.__stop_time = time()
        else:
            self.play_rush_sound()
            self.__rush_sound_time = time()

            if ((time() - self.stop_time) < 4.5):
                self.__stop = True
            else:
                self.__stop = False
                ship_x = self.game.ship.x
                ship_y = self.game.ship.y
                angle = atan2(ship_y-self.y, ship_x-self.x) 
                direction = int(180*angle/pi)

                self.__change_direction_time = time()-1
                self.set_speed(15)
                self.set_direction(direction)

                self.__rush_time = time()
                self.__activate_rush = False
                self.__invunerable = True
                self.__invunerable_time = time()

    def play_rush_sound(self):
        if ((time() - self.__rush_sound_time) > 8):
            self.game.get_sound_mixer().play_charge_tank_boss_rush_sfx()

    def red(self):
        if (self.invunerable == True) or (self.activate_rush == True):
            image = self.__tank_boss_rush_img
        else:
            image = self.__tank_boss_img

        self.set_original_image(image)

    def update_position(self) -> None:
        if (self.stop == False):
            super().update_position()

    def update(self) -> None:
        self.change_direction()
        self.red()
        self.rush()
        self.check_invunerable()
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
        
    @property
    def rush_time(self):
        return self.__rush_time

    @property
    def activate_rush(self):
        return self.__activate_rush

    @property
    def stop_time(self):
        return self.__stop_time

    @property
    def stop(self):
        return self.__stop
