import pygame
from os import path
from States.MainMenu import MainMenu
from States.SelectProfile import SelectProfile
from States.ProfileMenu import ProfileMenu
from States.Store import Store
from States.CreateProfile import CreateProfile
from States.NormalLevel import NormalLevel
from States.BossTransition import BossTransition
from States.BossLevel import BossLevel
from States.Result import Result
from States.Scoreboard import Scoreboard
from States.Introduction import Introduction
from States.Credits import Credits
from States.Settings import Settings
from Utility.GameData import GameData
from Utility.SoundMixer.SoundMixer import SoundMixer
from Utility.AnimationEffects.AnimationEffectsManager import AnimationEffectsManager

pasta = path.dirname(__file__)

class Game:
    def __init__(self, name = 'Asteroid'):
        pygame.init()
        self.__running = True
        self.__display_width = pygame.display.Info().current_w
        self.__display_height = pygame.display.Info().current_h
        self.__game_data = GameData()
        self.__sound_mixer = SoundMixer()
        self.__animation_effects_manager = AnimationEffectsManager()

        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        #dicionário com os estados do jogo
        self.__states_dictionary = {'MainMenu': MainMenu,
                                    'SelectProfile': SelectProfile,
                                    'CreateProfile': CreateProfile,
                                    'ProfileMenu': ProfileMenu,
                                    'Store': Store,
                                    'NormalLevel': NormalLevel,
                                    'BossTransition': BossTransition,
                                    'BossLevel': BossLevel,
                                    'Result': Result,
                                    'ScoreBoard': Scoreboard,
                                    'Credits': Credits,
                                    'Settings': Settings,
                                    'Introduction': Introduction 
                                   }
        #estado atual (começa no Introduction)
        self.__current_state = Introduction(self)
        
    def run(self):

        pygame.display.set_caption("ASTEROIDS")

        while self.running:
            self.handle_update()
            self.handle_transition()
        pygame.quit()
    
    #altera o estado atual com base na string que informa o nome do próximo estado
    def change_state(self, next_state_str: str):
        next_state = self.get_states_dictionary()[next_state_str](self)
        self.control_music(next_state)
        self.set_current_state(next_state)

    def control_music(self, next_state):
        next_state = next_state
    
        if (isinstance(next_state, NormalLevel)):
            self.__sound_mixer.play_normal_level_music()
        elif (isinstance(next_state, BossLevel)):
            self.__sound_mixer.play_boss_level_music()
        elif (isinstance(next_state, Result)):
            self.__sound_mixer.play_result_music()
        elif (isinstance(next_state, BossTransition)):
            pass
        else:
            if (isinstance(self.get_current_state(), Result)):
                self.__sound_mixer.play_theme_music()
            elif(isinstance(self.get_current_state(), Credits)):
                self.__sound_mixer.play_theme_music()
            elif(isinstance(self.get_current_state(), Introduction)):
                self.__sound_mixer.play_theme_music()

 
    def close(self):
        self.__running = False
        
    def get_current_state(self):
        return self.__current_state
    
    def set_current_state(self, next_state):
        self.__current_state = next_state
        
    def get_states_dictionary(self):
        return self.__states_dictionary
  
    def get_display(self):
        return self.display
    
    def handle_transition(self):
        return self.get_current_state().handle_transition()
    
    def handle_update(self):
        return self.get_current_state().handle_update()

    @property
    def animation_effects_manager(self):
        return self.__animation_effects_manager
        
    @property
    def sound_mixer(self):
        return self.__sound_mixer

    @property
    def game_data(self):
        return self.__game_data

    @property
    def display_width(self):
        return self.__display_width

    @property
    def display_height(self):
        return self.__display_height

    @property
    def running(self):
        return self.__running
 
