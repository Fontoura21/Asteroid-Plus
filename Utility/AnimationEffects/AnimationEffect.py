import pygame

class AnimationEffect(pygame.sprite.Sprite):
    def __init__(self, game, position: tuple, scale: tuple, animation_speed: int, looping: bool, list_imgs: list, direction: int = 0):
        super().__init__()

        self.__position = position
        self.__scale = scale
        self.__looping = looping
        self.__direction = direction

        self.__images_list = list_imgs
        self.__index = 0
        self.__counter_gap = 0
        self.__animation_speed = animation_speed

        img = self.__images_list[self.__index]
        image = pygame.transform.scale(img, self.__scale)
        self.__image = pygame.transform.rotate(image, self.direction)
        self.__mask = pygame.mask.from_surface(self.__image)
        self.__rect = self.image.get_rect()
        self.rect.center = self.__position

        game.all_sprites.add(self)

    def update(self):
        self.__counter_gap += 1
        if (self.__counter_gap >= self.__animation_speed):
            if (self.__index < (len(self.__images_list)-1)):
                self.__counter_gap = 0
                self.__index += 1
                img = self.__images_list[self.__index]
                image = pygame.transform.scale(img, self.__scale)
                self.__image = pygame.transform.rotate(image, self.direction)
                self.__mask = pygame.mask.from_surface(self.__image)

            if (self.__index >= (len(self.__images_list)-1)):
                if (self.__looping):
                    self.__index = 0
                else:
                    self.kill()

    def auto_kill(self):
        self.kill()

    def set_direction(self, direct: int):
        self.__direction = direct

    def hit(self):
        pass

    @property
    def direction(self):
        return self.__direction

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def mask(self):
        return self.__mask


