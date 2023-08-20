import pygame
from Utility.Utils.utils import *
from Entities.MovingEntities.MovingEntity import MovingEntity
from Utility.AnimationEffects.AnimationEffect import AnimationEffect
from random import randint
from time import time
from os import path
from math import atan2, pi, cos, sin, radians

pasta = get_folder_versao_top(__file__, 3)

class CannonBoss(MovingEntity):
    def __init__(self, game, life: int, position: tuple = None) -> None:
        self.__life = life
        self.__blast_animation: AnimationEffect = None

        self.__change_direction_time = time()
        self.__cannon_blast_time = time()
        self.__stop_time = time()
        self.__charge_up_sound_time = time()
        self.__cannon_blast_sound_time = time()
        self.__invunerable_time = time()

        self.__active_cannon_blast = False
        self.__stop = False
        self.__invunerable = False

        speed = 5
        direction = randint(0, 360)

        self.__invunerable_image = pygame.image.load(pasta+"//Images//Cannon_boss_invunerable.png")
        self.__cannon_boss_img = pygame.image.load(pasta+"//Images//Cannon_boss.png")
        super().__init__(game, speed, direction, self.__cannon_boss_img,  position)

    def hit(self) -> None:
        if ((not self.invunerable) and (not self.__active_cannon_blast)):
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

    def change_direction(self) -> None:
        if (not self.__active_cannon_blast):
            if ((time() - self.change_direction_time) > 3):
                self.__stop = False
                self.__active_cannon_blast = False
                self.destroi_laser_animation()
                self.game.get_sound_mixer().cannon_blast_sfx.stop()

                direction = randint(0, 360)
                self.set_speed(5)
                self.set_direction(direction)

                self.__change_direction_time = time()

    def update_image_position(self):
        self.set_image(pygame.transform.rotate(self.original_image, -self.direction))
        self.set_rect(self.image.get_rect(center=(self.x,self.y)))
        self.set_mask(pygame.mask.from_surface(self.image))

    def cannon_blast(self):
        if (self.__active_cannon_blast == False):
            if ((time() - self.__cannon_blast_time) > 8):
                self.__active_cannon_blast = True
                self.__stop_time = time()
        else:
            self.play_charge_up_sound()
            self.__charge_up_sound_time = time()

            if ((time() - self.__stop_time) < 4):
                self.__stop = True
                choice = 1 if (self.get_ship_angle() > self.direction) else -1
                inc_angle = abs(self.get_ship_angle() - self.direction)*choice/25
                self.set_direction(self.direction+inc_angle)
            else:
                self.play_cannon_blast_sound()
                laser_x = self.x + cos(radians(self.direction))*480
                laser_y = self.y + sin(radians(self.direction))*480
                self.__blast_animation = self.game.get_animation_effects_manager().add_laser_effect(game=self.game,
                                                                                                    position=(laser_x, laser_y),
                                                                                                    scale=(1000,100),
                                                                                                    direction= 180-self.direction,
                                                                                                    looping=True)
                self.game.boss_bullet_group.add(self.__blast_animation)
                self.__active_cannon_blast = False
                self.__cannon_blast_time = time()
                self.__change_direction_time = time()-1

    def play_charge_up_sound(self):
        if ((time() - self.__charge_up_sound_time) > 8):
            self.game.get_sound_mixer().play_charge_up_sfx()

    def play_cannon_blast_sound(self):
        if ((time() - self.__cannon_blast_sound_time) > 12):
            self.game.get_sound_mixer().play_cannon_blast_sfx()

    def check_invunerable(self):
        if (self.invunerable):
            if ((time() - self.__invunerable_time) > 2):
                self.__invunerable = False

    def get_ship_angle(self) -> int:
        ship_x = self.game.ship.x
        ship_y = self.game.ship.y
        angle = atan2(ship_y-self.y, ship_x-self.x)
        ship_angle = int(180*angle/pi)
        return ship_angle

    def update_position(self):
        if (not self.__stop):
            super().update_position()

    def destroi_laser_animation(self):
        try:
            self.__blast_animation.auto_kill()
        except:
            pass

    def red(self) -> None:
        if (self.__invunerable or self.__active_cannon_blast):
            self.set_original_image(self.__invunerable_image)
        else:
            self.set_original_image(self.__cannon_boss_img)
        

    def update(self) -> None:
        self.cannon_blast()
        self.change_direction()
        self.red()
        self.check_invunerable()
        super().update()

    def set_life(self, life: int):
        self.__life = life

    @property
    def invunerable(self):
        return self.__invunerable

    @property
    def change_direction_time(self):
        return self.__change_direction_time

    @property
    def life(self):
        return self.__life
        
