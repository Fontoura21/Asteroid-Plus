from abc import ABC, abstractmethod
import pygame
from math import cos, sin, radians
from random import randint

class MovingEntity(pygame.sprite.Sprite, ABC):
    def __init__(self, game, speed: float,
                 direction: int,
                 original_image,
                 position: tuple = None) -> None:
        super().__init__()

        #imagem original carregado
        self.__original_image = original_image

        #tamanho da tela
        self.__display_width = pygame.display.Info().current_w
        self.__display_height = pygame.display.Info().current_h

        #asteroidgame.py
        self.__game = game

        #posição inicial
        self.__x = 0
        self.__y = 0
        self.start_position(position)

        #velocidade
        self.__speed = speed
        self.__direction = direction

        self.load_image()

    @abstractmethod
    def hit(self) -> None:
        pass

    def start_position(self, position: tuple) -> None:
        if (position == None):
            random_side = randint(1,4)

            if (random_side == 1):
                self.__x = 0
                self.__y = randint(0, self.display_height)
            elif (random_side == 2):
                self.__x = randint(0, self.display_width)
                self.__y = 0
            elif (random_side == 2):
                self.__x = self.display_width
                self.__y = randint(0, self.display_height)
            else:
                self.__x = randint(0, self.display_width)
                self.__y = self.display_height

        else:
            self.__x = position[0]
            self.__y = position[1]


    def load_image(self):
        self.__image = self.original_image

        self.__rect = self.image.get_rect(center = (self.x, self.y))
        self.__mask = pygame.mask.from_surface(self.image)

    def update_image_position(self) -> None:
        self.__image = pygame.transform.rotate(self.original_image, self.direction)
        self.__rect = self.image.get_rect(center = (self.x, self.y))
        self.__mask = pygame.mask.from_surface(self.image)

    def update_position(self) -> None:
        self.__x += self.speed * cos(radians(self.direction))
        self.__y += self.speed * sin(radians(self.direction))

    def display_limit(self) -> None:
        if (self.x >= self.display_width):
            self.__x = 1
    
        if (self.x <= 0):
            self.__x = self.display_width-1

        if (self.y >= self.display_height):
            self.__y = 1

        if (self.y  <= 0):
            self.__y = self.display_height-1

    def update(self):
        self.display_limit()
        self.update_image_position()
        self.update_position()

    def set_direction(self, d):
        self.__direction = d

    def set_pos(self, x, y):
        self.__x = x
        self.__y = y

    def set_image(self, image):
        self.__image = image

    def set_rect(self, rect):
        self.__rect = rect

    def set_original_image(self, image: str):
        self.__original_image = image

    def set_speed(self, speed: float) -> None:
        self.__speed = speed
    
    def set_mask(self, mask):
        self.__mask = mask


    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def mask(self):
        return self.__mask

    @property
    def original_image(self):
        return self.__original_image

    @property
    def game(self):
        return self.__game

    @property
    def display_width(self):
        return self.__display_width

    @property
    def display_height(self):
        return self.__display_height

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def speed(self):
        return self.__speed

    @property
    def direction(self):
        return self.__direction

