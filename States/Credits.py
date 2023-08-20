import pygame
import webbrowser
from Entities.Button.Button import Button
from States.State import State


class Credits(State):
    def __init__(self, owner):
        super().__init__(owner)

        self.create_button()

    def create_button(self):
        x_pos = self.display_width // 2
        y_pos = self.display_height // 2

        back = Button(self, 20, 20, 180, 100, "<-- Back", True, self.back)
        self.all_sprites.add(back)

        buttonArthur = Button(self, self.x_pos-670, self.y_pos - 135, 120, 60, "GITHUB", True, self.gitArthur)
        self.all_sprites.add(buttonArthur)

        buttonBreno = Button(self, self.x_pos-670, self.y_pos-10, 120, 60, "GITHUB", True, self.gitBreno)
        self.all_sprites.add(buttonBreno)

        buttonLeonardo = Button(self, self.x_pos-670, self.y_pos + 115, 120, 60, "GITHUB", True, self.gitLeonardo)
        self.all_sprites.add(buttonLeonardo)

        buttonPedro = Button(self, self.x_pos-670, self.y_pos + 240, 120, 60, "GITHUB", True, self.gitPedro)
        self.all_sprites.add(buttonPedro)

        megaman = Button(self, self.x_pos+55, self.y_pos-135, 60, 60, "P", True, self.get_sound_mixer().play_theme_music)
        self.all_sprites.add(megaman)

        skyshark = Button(self, self.x_pos+55, self.y_pos-10, 60, 60, "P", True, self.get_sound_mixer().play_normal_level_music)
        self.all_sprites.add(skyshark)

        lufia2 = Button(self, self.x_pos+55, self.y_pos+115, 60, 60, "P", True, self.get_sound_mixer().play_boss_level_music)
        self.all_sprites.add(lufia2)

        smw = Button(self, self.x_pos+55, self.y_pos+240, 60, 60, "P", True, self.get_sound_mixer().play_result_music)
        self.all_sprites.add(smw)

    def back(self):
        self.get_owner().change_state("MainMenu")

    def gitArthur(self):
        url = "https://github.com/ArturRSoda"
        webbrowser.open_new(url)

    def gitBreno(self):
        url = "https://github.com/BrenoSPXx"
        webbrowser.open_new(url)

    def gitLeonardo(self):
        url = "https://github.com/leonardopfeng"
        webbrowser.open_new(url)

    def gitPedro(self):
        url = "https://github.com/Fontoura21"
        webbrowser.open_new(url)


    def screen_content(self):
        x_pos = self.display_width // 2
        y_pos = self.display_height // 2

        self.text("-=-=CREDITS=-=-", self.x_pos - 300, 20, 40, 'white')

        self.text("Creators", self.x_pos-490, self.y_pos-200, 40, "white")
        self.text("-Artur R. Soda", self.x_pos-545, self.y_pos - 125, 30, 'yellow')
        self.text("-Breno S. Pereira", self.x_pos - 545, self.y_pos, 30, 'yellow')
        self.text("-Leonardo Pfeng", self.x_pos - 545, self.y_pos + 125, 30, 'yellow')
        self.text("-Pedro A. Fontoura", self.x_pos - 545, self.y_pos + 250, 30, 'yellow')

        self.text("Musics", self.x_pos+200, self.y_pos-200, 40, "white")
        self.text("-Megaman 3 Theme", self.x_pos+120, self.y_pos-125, 25, "yellow")
        self.text("-Sky Shark NES Title Music", self.x_pos+120, self.y_pos, 25, "yellow")
        self.text("-Lufia2: Boss battle theme", self.x_pos+120, self.y_pos+125, 25, "yellow")
        self.text("-S.M.W.: Game Over music", self.x_pos+120, self.y_pos+250, 25, "yellow")


    def handle_update(self):
        pygame.display.update()
        self.background()
        self.screen_content()
        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())
        pygame.display.update()


    @property
    def x_pos(self):
        return self.display_width // 2

    @property
    def y_pos(self):
        return self.display_height // 2
