import pygame
from Profiles.Profile import Profile
from States.State import State
from Entities.Button.Button import Button

class Result(State):
    def __init__(self, owner):
        super().__init__(owner)
        self.save_data()
        self.create_button()

    def save_data(self):
        self.__credit_earned = (self.enemies_destroyed/10)*self.level
        score = 0 if (self.get_game_data().only_boss_mode) else self.score

        profile: Profile = self.get_game_data().profile
        max_score = max(score, profile.max_score)

        profile.set_credit(profile.credit+self.__credit_earned)
        profile.set_max_score(max_score)
        self.save_profile(profile)

    def screen_content(self):

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        self.text("-=-=RESULT=-=-", x_pos-280, y_pos-250, 50, "white")
        
        self.text("Level:", x_pos-200, y_pos - 100, 25, "white")
        self.text(str(self.level), x_pos-70, y_pos - 100, 25, "yellow")
        
        self.text("Enemies Destroyed:", x_pos-200, y_pos -50, 25, "white")
        self.text(str(self.enemies_destroyed), x_pos + 200, y_pos -50, 25, "yellow")
        
        self.text("Score:", x_pos-200, y_pos, 25, "white")
        self.text(str(self.score), x_pos-70, y_pos, 25, "yellow")

        self.text("Credit earned:", x_pos-200, y_pos+50, 25, "white")
        self.text("%.1f" % self.__credit_earned, x_pos+100, y_pos+50, 25, "yellow")

        message = "Score isnt't save when is Only-Boss-Mode" if (self.get_game_data().only_boss_mode) else ""
        self.text(message, x_pos-400, y_pos+120, 25, "red")


    def create_button(self) -> None:
        x_pos = self.display_width//2
        y_pos = self.display_height//2

        retry = Button(self, x_pos-310, y_pos+150, 300, 100, "RETRY", True, self.retry)
        self.all_sprites.add(retry)

        menu =Button(self, x_pos+10, y_pos+150, 300, 100, "MENU", True, self.menu)
        self.all_sprites.add(menu)
    
    def reset_data(self):
        self.get_game_data().set_enemies_destroyed(0) 
        self.get_game_data().set_level(1) 
        
        life = 3 + self.get_owner().game_data.profile.ship_life-1
        self.get_game_data().set_ship_life(life)
    
    def retry(self):
        self.reset_data()
        if (self.get_game_data().only_boss_mode):
            self.get_owner().change_state('BossTransition')
        else:
            self.get_owner().change_state('NormalLevel')
    
    def menu(self):
        self.reset_data()
        self.get_owner().change_state('ProfileMenu')
    

    def handle_update(self):
        pygame.display.update()
        self.background()
        self.screen_content()
        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())
        pygame.display.update()

    @property
    def level(self):
        return self.get_game_data().level

    @property
    def score(self):
        return self.get_game_data().score

    @property
    def enemies_destroyed(self):
        return self.get_game_data().enemies_destroyed

