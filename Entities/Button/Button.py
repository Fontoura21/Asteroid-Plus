from os import path
import pygame

pasta = path.dirname(path.dirname(path.dirname(__file__)))


class Button(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int, width: int, heigth: int, text: str, sound: bool, callback) -> None:
        super().__init__()

        self.__game = game
        self.__sound = sound

        self.__pressed = False

        self.__width = width
        self.__heigth = heigth

        self.__callback = callback
        self.__norm_image = pygame.Surface([self.width, self.heigth], pygame.SRCALPHA)
        pygame.draw.rect(self.__norm_image, (50,50,50), (0, 0, self.width, self.heigth))
        pygame.draw.rect(self.__norm_image, (5,5,5), (self.heigth*0.1, self.heigth*0.1, self.width-2*(self.heigth*0.1), self.heigth-2*(self.heigth*0.1)))

        self.__hover_image = pygame.Surface([self.width, self.heigth], pygame.SRCALPHA)
        pygame.draw.rect(self.__hover_image, (50, 50, 50), (0, 0, self.width, self.heigth))
        pygame.draw.rect(self.__hover_image, (150, 150, 150), (self.heigth*0.1, self.heigth*0.1, self.width-2*(self.heigth*0.1), self.heigth-2*(self.heigth*0.1)))

        self.__font = pygame.font.Font(pasta+"//assets//fonts//joystix.otf", 20)
        textSurface = self.__font.render(text, True, (0, 255, 255))
        textRect = textSurface.get_rect(center = (self.width//2, self.heigth//2))
        self.__norm_image.blit(textSurface, textRect)
        self.__hover_image.blit(textSurface, textRect)

        self.__image = self.__norm_image
        self.__rect = self.__image.get_rect(topleft=(x, y))

    def update(self) -> None:
        if self.__rect.collidepoint(pygame.mouse.get_pos()):
            self.__image = self.__hover_image
            if pygame.mouse.get_pressed()[0]:
                self.__pressed = True
            else:
                if (self.pressed == True):
                    self.__pressed = False
                    self.__callback()

                    if (self.__sound):
                        self.game.get_sound_mixer().play_button_click_sfx()
        else:
            self.__pressed = False
            self.__image = self.__norm_image

    @property
    def game(self):
        return self.__game

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def width(self):
        return self.__width

    @property
    def heigth(self):
        return self.__heigth

    @property
    def pressed(self):
        return self.__pressed
