import pygame
class Fade:
    def __init__(self, display_width: int, display_height: int) -> None:
        self.__surface = pygame.Surface((display_width, display_height))
        self.__alpha = None
        self.__fade_start = True
        self.__fade_end = False

    
    def fill_black(self) -> None:
        self.surface.fill((0,0,0))
    
    def alpha_count(self) -> bool:
        if self.fade_start:
            self.alpha -= 1
        else:
            self.alpha += 1
        if self.alpha == 0 or self.alpha == 255:
            return self.change_fade()
        else:
            return False
        
    
    def change_fade(self) -> bool:
        if self.fade_start:
            self.fade_end = True
            self.fade_start = False
            return False
        else:
            self.fade_end = False
            self.fade_start = True
            return True
        
    @property
    def alpha(self):
        return self.__alpha
    
    @property
    def fade_start(self):
        return self.__fade_start

    @property
    def fade_end(self):
        return self.__fade_end
    
    @property
    def surface(self):
        return self.__surface

    @alpha.setter
    def alpha(self, alpha: int) -> None:
        self.__alpha = alpha
        
    @fade_start.setter
    def fade_start(self, status: bool):
        self.__fade_start = status
    
    @fade_start.setter
    def fade_end(self, status: bool):
        self.__fade_end = status