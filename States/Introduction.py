import pygame
from States.State import State
import os
from Utility.Utils.utils import get_assets_path
from Utility.Utils.fade import Fade
from Entities.Button.Button import Button
class Introduction(State):
    def __init__(self, owner):
        super().__init__(owner)
        self.__intro_credits = pygame.font.Font(f'{get_assets_path(__file__)}/fonts/game_font.ttf', 70)
        self.__fade = Fade(self.display_width, self.display_height)
        self.__fade.fill_black()
        self.__fade.alpha = 255
        
        
        self.__intros = ['ABLP Company', 'IN ASSOCIATION WITH UFSC', 'PRESENT', 'ASTEROID-PLUS']
        self.__current_intro = self.intros[0]
        self.__intros_completed = 0
        self.__intro_ended = False

        self.create_button()


    def create_button(self) -> None:
        skip = Button(self, 10, 10, 100, 70, "SKIP", True, self.skip)
        self.all_sprites.add(skip)

    def skip(self):
        self.get_owner().change_state('MainMenu')
    
    def intro_content(self):
        self.intro_credits_surf = self.intro_credits.render(
            self.current_intro, True, 'Grey'
        )

        self.intro_credits_rect = self.intro_credits_surf.get_rect(
            center=(self.display_width / 2, 360)
        )
    
    def change_intro(self):
        if self.intros_completed < len(self.intros):
            self.current_intro = self.intros[self.intros_completed]
    
    #conteúdo da tela é formado pelas apresentações
    def screen_content(self):
        self.intro_content()
        pygame.event.get()
        self.fade.surface.set_alpha(self.fade.alpha)
        self.get_display().blit(self.intro_credits_surf, self.intro_credits_rect)
        self.get_display().blit(self.fade.surface, (0, 0))
        pygame.time.delay(8)
        self.intro_ended = self.fade.alpha_count() 
        if self.intro_ended:
            self.intros_completed += 1
            self.change_intro()
    
    #após a introdução vai para o menu principal
    def handle_transition(self):
        super().handle_transition()
        if self.intros_completed == len(self.intros) and self.intro_ended:
            self.get_owner().change_state('MainMenu')

    
    def handle_update(self):
        pygame.display.update()
        self.screen_content()
        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())
        pygame.display.update()

    
    @property
    def intro_credits(self):
        return self.__intro_credits  
    
    @property
    def fade(self):
        return self.__fade
    
    @property
    def intros(self):
        return self.__intros
    
    @property
    def current_intro(self):
        return self.__current_intro
    
    @property
    def intro_quant(self):
        return self.__intro_quant
    
    @property
    def intro_ended(self):
        return self.__intro_ended
    
    @property
    def intros_completed(self) -> int:
        return self.__intros_completed

    @intros_completed.setter
    def intros_completed(self, intros_completed: int):
        self.__intros_completed = intros_completed
    
    @current_intro.setter
    def current_intro(self, next_intro: str):
        self.__current_intro = next_intro   
    
    @intro_ended.setter
    def intro_ended(self, bool_value: bool):
        self.__intro_ended = bool_value
 
 