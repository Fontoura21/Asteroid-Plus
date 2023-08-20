import pygame
from Entities.Button.Button import Button
from States.State import State


class MainMenu(State):
    def __init__(self, owner):
        super().__init__(owner)
        self.__all_sprites = pygame.sprite.Group()

        self.create_button()

    def create_button(self):

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        #menu buttons
        newProfile = Button(self, x_pos-310, y_pos - 170, 300, 100, 'New Profile', True, self.new_profile)
        self.all_sprites.add(newProfile)

        selectProfile = Button(self, x_pos+10, y_pos-170, 300, 100, 'Select Profile', True, self.select_profile)
        self.all_sprites.add(selectProfile)

        scoreboard = Button(self, x_pos-310, y_pos-20, 300, 100, 'Scoreboard', True, self.scoreboard)
        self.all_sprites.add(scoreboard)

        credits = Button(self, x_pos+10, y_pos-20, 300, 100, 'Credits', True, self.credits)
        self.all_sprites.add(credits)

        settings = Button(self, x_pos-150, y_pos+130, 300, 100, 'Settings', True, self.settings)
        self.all_sprites.add(settings)

        quit = Button(self, x_pos-150, y_pos+280, 300, 100, 'Quit', True, self.quit)
        self.all_sprites.add(quit)

    def select_profile(self):
        self.get_owner().change_state("SelectProfile")

    def new_profile(self):
        self.get_owner().change_state("CreateProfile")

    def quit(self):
        self.get_owner().close()

    def scoreboard(self):
        self.get_owner().change_state("ScoreBoard")

    def credits(self):
        self.get_owner().change_state("Credits")

    def settings(self):
        self.get_owner().change_state("Settings")

    def screen_content(self):

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        self.text("-=-=ASTEROIDS-PLUS=-=-", x_pos-400, 100, 45, "white")

    @property
    def all_sprites(self):
        return self.__all_sprites

    def handle_update(self):
        pygame.display.update()
        self.background()
        self.screen_content()
        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())
        pygame.display.update()
