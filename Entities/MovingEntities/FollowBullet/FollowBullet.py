import pygame
from os import path
from Utility.Utils.utils import *
from Entities.MovingEntities.MovingEntity import MovingEntity
from math import atan2, pi, cos, sin, radians
from time import time

pasta = get_folder_versao_top(__file__, 3)

class FollowBullet(MovingEntity):
    def __init__(self, game,
                 position: tuple,
                 direction: int,
                 speed: float,
                 damage: int,
                 lifetime: int) -> None:

        #dano e tempo de vida
        self.__damage = damage
        self.__lifetime = lifetime  
        self.__dx = 0
        self.__dy = 0
        self.__smoke_time = time()

        #tempo de criação
        self.__init_time = time()

        img = pygame.image.load(pasta+"//Images//follow_bullet.png")
        super().__init__(game, speed, direction, img, position)

    def update_image_position(self) -> None:
        image = pygame.transform.rotate(self.original_image, -self.direction)
        self.set_image(image)
        self.set_rect(self.image.get_rect(center = (self.x, self.y)))
        self.set_mask(pygame.mask.from_surface(self.image))

    def accelerate(self):
        vel_max = 10
        self.__dx += cos(radians(self.direction)) * self.speed/8
        self.__dy += sin(radians(self.direction)) * self.speed/8

        if (abs(self.__dx) > vel_max):
            self.__dx = -vel_max if (self.__dx < 0) else vel_max
        if (abs(self.__dy) >= vel_max):
            self.__dy = -vel_max if (self.__dy < 0) else vel_max

    def update_position(self):
        self.__dx /= 1.01
        self.__dy /= 1.01

        x = self.x + self.__dx
        y = self.y + self.__dy
        self.set_pos(x, y)

    def update_direction(self):
        ship_x = self.game.ship.x
        ship_y = self.game.ship.y
        angle = atan2(ship_y-self.y, ship_x-self.x)
        ship_angle = int(180*angle/pi)
        self.set_direction(ship_angle)

    def hit(self) -> None:
        self.kill()

    def detect_lifetime(self) -> None:
        if (time() - self.__init_time > self.lifetime):
            self.game.get_sound_mixer().play_explosion_2_sfx()
            self.game.get_animation_effects_manager().add_explosion_effect(game=self.game,
                                                                           position=(self.x,self.y),
                                                                           scale=(50,50),
                                                                           looping=False,
                                                                           speed=7)
            self.kill()

    def add_smoke_effect(self):
        if ((time() - self.__smoke_time) > 0.05):
            x = self.x - cos(radians(self.direction))*20
            y = self.y - sin(radians(self.direction))*20
            self.game.get_animation_effects_manager().add_smoke_effect(game=self.game,
                                                                    position=(x,y),
                                                                    scale=(10,10),
                                                                    looping=False)
            self.__smoke_time = time()


    def update(self) -> None:
        self.detect_lifetime()
        self.update_direction()
        self.accelerate()
        self.add_smoke_effect()
        super().update()


    @property
    def damage(self):
        return self.__damage

    @property
    def lifetime(self):
        return self.__lifetime
    
    @property
    def init_time(self):
        return self.__init_time
