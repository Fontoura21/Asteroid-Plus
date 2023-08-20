import pygame
from Profiles.Profile import Profile
from States.State import State
from time import time

class BossTransition(State):
    def __init__(self, owner):
        super().__init__(owner)

        self.__init_time = time()
        self.__blink_time = time()
        self.__text_color = "gray"

        if (self.only_boss_mode):
            self.__enter_boss_fight = True
        else:
            self.__enter_boss_fight = True if ((self.level-1) % 5 == 4) else False

        self.sfx()

        self.__profile: Profile = self.get_owner().game_data.profile
        self.create_button()

    def create_button(self):
        pass

    def sfx(self):
        pygame.mixer.fadeout(1000)
        if (self.enter_boss_fight):
            self.get_sound_mixer().play_boss_fight_sfx()
        else:
            self.get_sound_mixer().play_boss_defeated_sfx()

    def screen_content(self) -> None:

        self.blink_text()

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        if (self.enter_boss_fight):
            self.text("BOSS FIGHT", x_pos-200, y_pos-50, 50, self.text_color)
        else:
            self.text("BOSS DEFEATED", x_pos-280, y_pos-50, 50, self.text_color)

    def blink_text(self) -> None:
        if ((time() - self.blink_time) >= 0.5):
            if (self.enter_boss_fight):
                self.__text_color = "red" if (self.text_color == "gray") else "gray"
            else:
                self.__text_color = "green" if (self.text_color == "gray") else "gray"

            self.__blink_time = time()

    def transition(self):
        if ((time() - self.init_time) > 7):
            if (self.enter_boss_fight):
                self.get_owner().change_state("BossLevel")
            else:
                self.get_owner().change_state("NormalLevel")

    def handle_update(self) -> None:
        pygame.display.update()
        self.background()
        self.screen_content()
        self.transition()
        pygame.display.update()

    

    @property
    def profile(self) -> Profile:
        return self.__profile

    @property
    def blink_time(self):
        return self.__blink_time

    @property
    def text_color(self):
        return self.__text_color

    @property
    def init_time(self):
        return self.__init_time

    @property
    def level(self):
        return self.get_game_data().level

    @property
    def enemies_destroyed(self):
        return self.get_game_data().enemies_destroyed

    @property
    def only_boss_mode(self):
        return self.get_game_data().only_boss_mode

    @property
    def enter_boss_fight(self):
        return self.__enter_boss_fight