import pygame
from Entities.Button.Button import Button
from States.State import State


class Scoreboard(State):
    def __init__(self,owner):
        super().__init__(owner)

        self.create_button()
               

    def create_button(self):

        x_pos = self.display_width//2 - 150
        y_pos = self.display_height//2

        back = Button(self, 20, 20, 180, 100, "<-- Back", True, self.back)
        self.all_sprites.add(back)


    def back(self):
        self.get_owner().change_state("MainMenu")

    def screen_content(self):

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        self.text("-=-=SCOREBOARD=-=-", x_pos-300, y_pos-270, 40, 'white')

        name1 = self.get_all_profiles()[0].name if (len(self.get_all_profiles()) >= 1) else "<None>"
        self.text("1. %s" % (name1), x_pos-350, y_pos-125, 40, 'yellow')

        name2 = self.get_all_profiles()[1].name if (len(self.get_all_profiles()) >= 2) else "<None>"
        self.text("2. %s" % (name2), x_pos-350, y_pos-55, 40, 'yellow')

        name3 = self.get_all_profiles()[2].name if (len(self.get_all_profiles()) >= 3) else "<None>"
        self.text("3. %s" % (name3), x_pos-350, y_pos+15, 40, 'yellow')

        name4 = self.get_all_profiles()[3].name if (len(self.get_all_profiles()) >= 4) else "<None>"
        self.text("4. %s" % (name4), x_pos-350, y_pos+85, 40, 'yellow')

        name5 = self.get_all_profiles()[4].name if (len(self.get_all_profiles()) >= 5) else "<None>"
        self.text("5. %s" % (name5), x_pos-350, y_pos+155, 40, 'yellow')

        score1 = self.get_all_profiles()[0].max_score if (len(self.get_all_profiles()) >= 1) else ""
        self.text("%s" % (score1), x_pos+50, y_pos-125, 40, 'yellow')

        score2 = self.get_all_profiles()[1].max_score if (len(self.get_all_profiles()) >= 2) else ""
        self.text("%s" % (score2), x_pos+50, y_pos-55, 40, 'yellow')

        score3 = self.get_all_profiles()[2].max_score if (len(self.get_all_profiles()) >= 3) else ""
        self.text("%s" % (score3), x_pos+50, y_pos+15, 40, 'yellow')

        score4 = self.get_all_profiles()[3].max_score if (len(self.get_all_profiles()) >= 4) else ""
        self.text("%s" % (score4), x_pos+50, y_pos+85, 40, 'yellow')

        score5 = self.get_all_profiles()[4].max_score if (len(self.get_all_profiles()) >= 5) else ""
        self.text("%s" % (score5), x_pos+50, y_pos+155, 40, 'yellow')

    def handle_update(self):
        pygame.display.update()
        self.background()
        self.screen_content()
        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())
        pygame.display.update()