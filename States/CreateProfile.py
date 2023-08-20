import pygame
from os import path
from Entities.Button.Button import Button
from States.State import State
from tkinter import messagebox

pasta = path.dirname(path.dirname(__file__))

class CreateProfile(State):
    def __init__(self, owner) -> None:
        super().__init__(owner)
        self.__name = ''
        self.__name_max_length = 5

        x = (self.display_width//2)-150
        y = (self.display_height//2)-100
        self.__input_box = pygame.Rect(x, y, 300, 100)
        self.__box_color = (50, 50, 50)
        self.__active_box = False

        self.create_button()


    def screen_content(self) -> None:

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        self.__box_color = (100, 100, 100) if (self.active_box) else (50, 50, 50)
        pygame.draw.rect(self.get_display(), self.box_color, self.input_box)
        self.update_input_box()
        
        self.text("ENTER A NEW NAME", x_pos-315, y_pos-250, 50, "white")
    
    
    def create_button(self) -> None:
        x_pos = self.display_width//2
        y_pos = self.display_height//2

        select = Button(self, x_pos-310, y_pos+150, 300, 100, "Create", True, self.call_create_profile)
        self.all_sprites.add(select)

        back = Button(self, x_pos+10, y_pos+150, 300, 100, "Back", True, self.back)
        self.all_sprites.add(back)

    #chama a função create profile, caso os requisitos sejam cumpridos, senão mostra mensagens de erro
    def call_create_profile(self) -> None:
        if len(self.name) != 0:
            if len(self.name) <= self.name_max_length:
                if " " not in self.name:
                    if not self.verify_profile_existence(self.name):
                        self.create_profile(self.name, 0, 0, 1, 1, 1, 1, 1)
                        self.enter_selected_profile()
                    else:
                        messagebox.showerror(title = 'ERROR', message = f"{self.name} already exists")
                else:
                    messagebox.showerror(title = 'ERROR', message = "The name should not have spaces")
            else:
                messagebox.showerror(title = 'ERROR', message = f"{self.name} should have less than {self.name_max_length} characters")
        else:
            messagebox.showerror(title = 'ERROR', message = "The name should have a bigger length")
    

    #entra no perfil criado e vai para a tela de menu do usuário
    def enter_selected_profile(self) -> None:
        if (len(self.all_profiles) != 0):
            self.get_owner().game_data.set_profile(self.profile_selected)
            self.get_owner().change_state("ProfileMenu")

    #volta para o menu principal
    def back(self) -> None:
        self.get_owner().change_state("MainMenu")

    def update_input_box(self):
        font = pygame.font.Font(pasta+"//assets//fonts//joystix.otf", 40)
        if (self.active_box):
            name = self.name
        else:
            name = "<name>" if (self.name == "") else self.name
        text_surface = font.render(name, True, "yellow")
        text_rect = text_surface.get_rect(center = (self.display_width//2, (self.display_height//2)-50))
        self.get_display().blit(text_surface, text_rect)

    def handle_update(self) -> None:
        pygame.display.update()
        self.background()
        self.screen_content()
        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())
        pygame.display.update()

    def handle_transition(self):
        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONDOWN):
                self.__active_box = True if (self.input_box.collidepoint(event.pos)) else False

            if (event.type == pygame.KEYDOWN):
                if (self.active_box):
                    if (event.key == pygame.K_BACKSPACE):
                        self.__name = self.name[:-1]
                    elif (event.key == pygame.K_ESCAPE):
                        self.__active_box = False
                    elif (event.key == pygame.K_RETURN):
                        pass
                    else:
                        if (len(self.name) < self.name_max_length):
                            self.__name += event.unicode

    @property
    def active_box(self):
        return self.__active_box

    @property
    def box_color(self):
        return self.__box_color

    @property
    def all_profiles(self) -> list:
        return self.get_all_profiles()

    @property
    def input_box(self):
        return self.__input_box
    
    @property
    def name_max_length(self):
        return self.__name_max_length
    
    @property
    def name(self):
        return self.__name    
    
    @property
    def profile_selected(self):
        return self.all_profiles[-1]   
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    @input_box.setter
    def input_box(self, input_box):
        self.__input_box = input_box