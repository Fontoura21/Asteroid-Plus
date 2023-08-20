import pygame
from Entities.Button.Button import Button
from States.State import State
from tkinter import messagebox

class SelectProfile(State):
    def __init__(self, owner) -> None:
        super().__init__(owner)
        self.create_button()

        self.__profile_selected_index = 0

    def screen_content(self) -> None:

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        
        self.text("SELECT YOUR PROFILE", x_pos-400, y_pos-250, 50, "white")
        self.show_profile_selected_name()

    def show_profile_selected_name(self) -> None:

        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        if (len(self.all_profiles) == 0):
            self.text("None", x_pos-80, y_pos-70, 40, "yellow")
        else:
            self.text(self.profile_selected.name , x_pos-80, y_pos-70, 40, "yellow")

    def create_button(self) -> None:
        x_pos = self.display_width//2
        y_pos = self.display_height//2

        back = Button(self, 20, 20, 180, 100, "<-- Back", True, self.back)
        self.all_sprites.add(back)

        advance = Button(self, x_pos+100, y_pos-80, 100, 70, ">>>", True, self.advance_selected_profile)
        self.all_sprites.add(advance)

        back = Button(self, x_pos-200, y_pos-80, 100, 70, "<<<", True, self.back_selected_profile)
        self.all_sprites.add(back)

        select = Button(self, x_pos-310, y_pos+150, 300, 100, "Enter Profile", True, self.enter_selected_profile)
        self.all_sprites.add(select)

        remove =Button(self, x_pos+10, y_pos+150, 300, 100, "Remove Profile", True, self.remove_selected_profile)
        self.all_sprites.add(remove)

    def remove_selected_profile(self) -> None:
        if (len(self.all_profiles) != 0):
            if (messagebox.askyesno("Remove Profile", "Do you really want to delete %s profile?" % self.profile_selected.name)):
                self.remove_profile(self.profile_selected.name)
                self.advance_selected_profile()


    def enter_selected_profile(self) -> None:
        if (len(self.all_profiles) != 0):
            self.get_owner().game_data.set_profile(self.profile_selected)
            self.get_owner().change_state("ProfileMenu")

    def advance_selected_profile(self) -> None:
        if (len(self.all_profiles) == 0):
            self.__profile_selected_index = 0
        elif (self.profile_selected_index >= len(self.all_profiles)-1):
            self.__profile_selected_index = 0
        else:
            self.__profile_selected_index += 1

    def back_selected_profile(self) -> None:
        if (len(self.all_profiles) == 0):
            self.__profile_selected_index = 0
        elif (self.profile_selected_index == 0):
            self.__profile_selected_index = len(self.all_profiles)-1
        else:
            self.__profile_selected_index -= 1

    def back(self) -> None:
        self.get_owner().change_state("MainMenu")


    def handle_update(self) -> None:
        pygame.display.update()
        self.background()
        self.screen_content()
        pygame.display.update()

    @property
    def all_profiles(self) -> list:
        return self.get_all_profiles()

    @property
    def profile_selected_index(self) -> int:
        return self.__profile_selected_index

    @property
    def profile_selected(self):
        return self.all_profiles[self.profile_selected_index]
       