import pygame
from Entities.MovingEntities.MovingEntity import MovingEntity
from Entities.MovingEntities.Bullet.Bullet import Bullet
from random import randint
from time import time


class BasicEnemy(MovingEntity):
    def __init__(self, game, img, life: int, position: tuple = None) -> None:
        self.__life = life

        self.__change_direction_time = time()
        self.__last_shoot_time = time()

        speed = randint(2, 4)
        direction = randint(0, 360)
        original_image = img
        super().__init__(game, speed, -direction, original_image, position)

    def hit(self) -> None:
        self.__life -= 1
        if (self.life <= 0):
            self.game.get_animation_effects_manager().add_explosion_effect(game=self.game,
                                                                            position=(self.x,self.y),
                                                                            scale=(45, 45),
                                                                            looping=False,
                                                                            speed=5)

            self.game.get_sound_mixer().play_basic_enemy_explosion_sfx()

            self.kill()

    def shoot(self) -> None:
        if ((time() - self.last_shoot_time) > 2):
            direction = randint(0, 360)

            bullet = Bullet(self, (self.x, self.y), direction, 10, 1, "red", 1)
            self.game.all_sprites.add(bullet)
            self.game.basic_enemy_bullet_group.add(bullet)

            self.__last_shoot_time = time()
    
    def update_image_position(self) -> None:
        self.set_image(self.original_image)
        self.set_rect(self.image.get_rect(center = (self.x, self.y)))
        self.set_mask(pygame.mask.from_surface(self.image))

    def change_direction(self) -> None:
        if ((time() - self.change_direction_time) > 5):

            direction = randint(0, 360)
            self.set_direction(direction)

            self.__change_direction_time = time()

    def update(self) -> None:
        self.change_direction()
        self.shoot()
        super().update()

    @property
    def last_shoot_time(self):
        return self.__last_shoot_time

    @property
    def change_direction_time(self):
        return self.__change_direction_time

    @property
    def life(self):
        return self.__life
