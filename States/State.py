import pygame
from os import path
from Profiles.ProfileManager import ProfileDAO
from Profiles.Profile import Profile
from abc import ABC, abstractmethod

pasta = path.dirname(path.dirname(__file__))

class State(ABC):
    def __init__(self, owner):
        #Game é o parâmetro owner. Assim é possível fazer a transição de estados com o change_state
        self.__owner = owner

        #altura e largura da tela
        self.__display_width = pygame.display.Info().current_w
        self.__display_height = pygame.display.Info().current_h

        #background images
        img = pygame.image.load(pasta+"//Images//background.png")
        img = pygame.transform.scale(img, (self.display_width, self.display_height))
        self.__background = img
        self.__b_pos = 0
        self.__overlap = img
        self.__o_pos = self.display_width
 
        #todos os sprites
        self.__all_sprites = pygame.sprite.Group()

    def background(self, speed: int = 0.2):
        if (self.__b_pos <= -self.display_width):
            self.__b_pos = self.display_width
        if (self.__o_pos <= -self.display_width):
            self.__o_pos = self.display_width

        self.__b_pos -= speed
        self.__o_pos -= speed

        self.get_display().blit(self.__background, (self.__b_pos, 0))
        self.get_display().blit(self.__overlap, (self.__o_pos, 0))


    def get_display(self):
        return pygame.display.get_surface()

    def get_owner(self):
        return self.__owner
    
    def get_game_data(self):
        return self.__owner.game_data
        
    def get_sound_mixer(self):
        return self.__owner.sound_mixer

    def get_animation_effects_manager(self):
        return self.__owner.animation_effects_manager

    def get_all_sprites(self):
        return self.__all_sprites

    #verifica se o perfil existe pelo nome
    #True -> perfil existe
    #False -> perfil não existe
    def verify_profile_existence(self, name: str) -> bool:
        return ProfileDAO().verify_profile_existence(name)

    #retorna um perfil pelo nome
    #retorna o perfil se existir
    # se o perfil NAO existir retorna FALSE
    def get_profile(self, name: str) -> Profile:
        return ProfileDAO().get_profile(name)

    #retora uma lista ORDENADA de todos os perfils
    def get_all_profiles(self) -> list[Profile]:
        return ProfileDAO().get_all_profiles()

    #remove um perfil pelo nome
    #True -> removido com sucesso
    #False -> perfil não existe
    def remove_profile(self, profile: str) -> bool:
        return ProfileDAO().remove_profile(profile)

    #salva um perfil ja existente
    #True -> salvado com sucesso
    #False -> Perfil não existe
    def save_profile(self, profile: Profile) -> bool:
        return ProfileDAO().save_profile(profile)

    #cria um novo perfil
    #Dá erro se o perfil já existir
    def create_profile(self, name: str,
                       credit: int,
                       max_score: int,
                       ship_damage: int,
                       ship_vel_max: float,
                       ship_life: int,
                       ship_cooldown: int,
                       ship_qtd_bullet: int) -> None:
        return ProfileDAO().create_profile(name, credit, max_score, ship_damage, ship_vel_max, ship_life, ship_cooldown, ship_qtd_bullet)
    

    #metodo geral para colocar texto
    def text(self, text: str, x: int, y: int, size: int, color: str):
        self.font = pygame.font.Font(pasta+"//assets//fonts//joystix.otf", size)
        textSurface = self.font.render(text, True, (color))
        self.get_display().blit(textSurface, (x, y))

     #lida com a transição de estados
    def handle_transition(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.get_owner().close()
   
    #conteúdo da tela
    @abstractmethod
    def screen_content(self):
        pass

    #atualiza a tela
    @abstractmethod
    def handle_update(self):
        pass


    @property
    def display_width(self):
        return self.__display_width
    
    @property
    def display_height(self):
        return self.__display_height

    @property
    def all_sprites(self):
        return self.__all_sprites