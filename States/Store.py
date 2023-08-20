#oh-my-posh init pwsh | Invoke-Expression
import pygame
from Entities.Button.Button import Button
from States.State import State
from Profiles.Profile import Profile

class Store(State):
    def __init__(self, owner):
        super().__init__(owner)

        self.__cooldown_price = 30
        self.__vel_max_price = 15
        self.__damage_price = 20
        self.__life_price = 50
        self.__qtd_bullet_price = 40

        self.__current_profile: Profile = self.get_owner().game_data.profile

        self.create_button()

    def create_button(self):
        x_pos = self.display_width//2 
        y_pos = self.display_height//2

        back = Button(self, 20, 20, 180, 100, "<-- Back", True, self.back)
        self.all_sprites.add(back)

        # #linha 1 coluna 1
        # rmv_vel_max = Button(self, 20, 180, 70, 70, "-", True, self.rmv_vel_max)
        # add_vel_max = Button(self, 325, 180, 70, 70, "+", True, self.add_vel_max)
        # self.all_sprites.add(rmv_vel_max)
        # self.all_sprites.add(add_vel_max)

        #linha 1 coluna 1
        rmv_vel_max = Button(self, self.x_pos - 505 , self.y_pos - 220, 70, 70, "-", True, self.rmv_vel_max)
        add_vel_max = Button(self, self.x_pos - 200, self.y_pos - 220, 70, 70, "+", True, self.add_vel_max)
        self.all_sprites.add(rmv_vel_max)
        self.all_sprites.add(add_vel_max)

        # #linha 1 coluna 2
        # rmv_damage = Button(self, 500, 180, 70, 70, "-", True, self.rmv_damage)
        # add_damage = Button(self, 805, 180, 70, 70, "+", True, self.add_damage)
        # self.all_sprites.add(rmv_damage)
        # self.all_sprites.add(add_damage)

        #linha 1 coluna 2
        rmv_damage = Button(self, self.x_pos + 200, self.y_pos - 220, 70, 70, "-", True, self.rmv_damage)
        add_damage = Button(self, self.x_pos + 505, self.y_pos - 220, 70, 70, "+", True, self.add_damage)
        self.all_sprites.add(rmv_damage)
        self.all_sprites.add(add_damage)

        # #linha 2 coluna 1
        # rmv_life = Button(self, 20, 360, 70, 70, "-", True, self.rmv_life)
        # add_life = Button(self, 325, 360, 70, 70, "+", True, self.add_life)
        # self.all_sprites.add(rmv_life)
        # self.all_sprites.add(add_life)

        #linha 2 coluna 1
        rmv_life = Button(self, self.x_pos - 505, self.y_pos - 70, 70, 70, "-", True, self.rmv_life)
        add_life = Button(self, self.x_pos - 200, self.y_pos - 70, 70, 70, "+", True, self.add_life)
        self.all_sprites.add(rmv_life)
        self.all_sprites.add(add_life)

        # # linha 2 coluna 2
        # rmv_cooldown = Button(self, 500, 360, 70, 70, "-", True, self.rmv_cooldown)
        # add_cooldown = Button(self, 805, 360, 70, 70, "+", True, self.add_cooldown)
        # self.all_sprites.add(rmv_cooldown)
        # self.all_sprites.add(add_cooldown)

        # linha 2 coluna 2
        rmv_cooldown = Button(self, self.x_pos + 200, self.y_pos - 70, 70, 70, "-", True, self.rmv_cooldown)
        add_cooldown = Button(self, self.x_pos + 505, self.y_pos - 70, 70, 70, "+", True, self.add_cooldown)
        self.all_sprites.add(rmv_cooldown)
        self.all_sprites.add(add_cooldown)

        #linha 3
        rmv_qtd_bullet = Button(self, self.x_pos - 162, self.y_pos + 80, 70, 70, "-", True, self.rmv_qtd_bullet)
        add_qtd_bullet = Button(self, self.x_pos + 142, self.y_pos + 80, 70, 70, "+", True, self.add_qtd_bullet)
        self.all_sprites.add(rmv_qtd_bullet)
        self.all_sprites.add(add_qtd_bullet)




    def rmv_vel_max(self):
        if (self.current_profile.ship_vel_max > 1):

            credit = self.current_profile.credit + self.vel_max_price
            self.current_profile.set_credit(credit)

            vel_max = self.current_profile.ship_vel_max - 1
            self.current_profile.set_ship_vel_max(vel_max)

    def add_vel_max(self):
        if (self.current_profile.credit >= self.vel_max_price):
            if (self.current_profile.ship_vel_max < 5):

                credit = self.current_profile.credit - self.vel_max_price
                self.current_profile.set_credit(credit)

                vel_max = self.current_profile.ship_vel_max + 1
                self.current_profile.set_ship_vel_max(vel_max)

    def rmv_damage(self):
        if (self.current_profile.ship_damage > 1):

            credit = self.current_profile.credit + self.damage_price
            self.current_profile.set_credit(credit)

            damage = self.current_profile.ship_damage - 1
            self.current_profile.set_ship_damage(damage)

    def add_damage(self):
        if (self.current_profile.credit >= self.damage_price):
            if (self.current_profile.ship_damage < 5):

                credit = self.current_profile.credit - self.damage_price
                self.current_profile.set_credit(credit)

                damage = self.current_profile.ship_damage + 1
                self.current_profile.set_ship_damage(damage)

    def rmv_life(self):
        if (self.current_profile.ship_life > 1):

            credit = self.current_profile.credit + self.life_price
            self.current_profile.set_credit(credit)

            life = self.current_profile.ship_life - 1
            self.current_profile.set_ship_life(life)

    def add_life(self):
        if (self.current_profile.credit >= self.life_price):
            if (self.current_profile.ship_life < 5):

                credit = self.current_profile.credit - self.life_price
                self.current_profile.set_credit(credit)

                life = self.current_profile.ship_life + 1
                self.current_profile.set_ship_life(life)


    def rmv_cooldown(self):
        if (self.current_profile.ship_cooldown > 1):

            credit = self.current_profile.credit + self.cooldown_price
            self.current_profile.set_credit(credit)

            cooldown = self.current_profile.ship_cooldown - 1
            self.current_profile.set_ship_cooldown(cooldown)

    def add_cooldown(self):
        if(self.current_profile.credit >= self.cooldown_price):
            if(self.current_profile.ship_cooldown < 5):

                credit = self.current_profile.credit - self.cooldown_price
                self.current_profile.set_credit(credit)

                cooldown = self.current_profile.ship_cooldown + 1
                self.current_profile.set_ship_cooldown(cooldown)

    def rmv_qtd_bullet(self):
        if (self.current_profile.ship_qtd_bullet > 1):

            credit = self.current_profile.credit + self.qtd_bullet_price
            self.current_profile.set_credit(credit)

            qtd_bullet = self.current_profile.ship_qtd_bullet - 1
            self.current_profile.set_ship_qtd_bullet(qtd_bullet)


    def add_qtd_bullet(self):
        if (self.current_profile.credit >= self.qtd_bullet_price):
            if (self.current_profile.ship_qtd_bullet < 5):
                credit = self.current_profile.credit - self.qtd_bullet_price
                self.current_profile.set_credit(credit)

                qtd_bullet = self.current_profile.ship_qtd_bullet + 1
                self.current_profile.set_ship_qtd_bullet(qtd_bullet)




    def update_rects(self) -> None:
        self.vel_max_rect()
        self.damage_rect()
        self.life_rect()
        self.cooldown_rect()
        self.qtd_bullet_rect()

    def vel_max_rect(self):
        #1 rect
        self.rect(self.x_pos - 425, self.y_pos - 200, 50, 25, self.current_profile.ship_vel_max, 2)
        #2 rect
        self.rect(self.x_pos - 370, self.y_pos - 200, 50, 25, self.current_profile.ship_vel_max, 3)
        #3 rect
        self.rect(self.x_pos - 315, self.y_pos - 200, 50, 25, self.current_profile.ship_vel_max, 4)
        #4 rect
        self.rect(self.x_pos - 260, self.y_pos - 200, 50, 25, self.current_profile.ship_vel_max, 5)

    def damage_rect(self):
        #1 rect
        self.rect(self.x_pos + 280, self.y_pos - 200, 50, 25, self.current_profile.ship_damage, 2)
        #2 rect
        self.rect(self.x_pos + 335, self.y_pos - 200, 50, 25, self.current_profile.ship_damage, 3)
        #3 rect
        self.rect(self.x_pos + 390, self.y_pos - 200, 50, 25, self.current_profile.ship_damage, 4)
        #4 rect
        self.rect(self.x_pos + 445, self.y_pos - 200, 50, 25, self.current_profile.ship_damage, 5)

    def life_rect(self):
        #1 rect
        self.rect(self.x_pos - 425, self.y_pos - 50, 50, 25, self.current_profile.ship_life, 2)
        #2 rect
        self.rect(self.x_pos - 370, self.y_pos - 50, 50, 25, self.current_profile.ship_life, 3)
        #3 rect
        self.rect(self.x_pos - 315, self.y_pos - 50, 50, 25, self.current_profile.ship_life, 4)
        #4 rect
        self.rect(self.x_pos - 260, self.y_pos - 50, 50, 25, self.current_profile.ship_life, 5)

    def cooldown_rect(self):
        # 1 rect
        self.rect(self.x_pos + 280, self.y_pos - 50, 50, 25, self.current_profile.ship_cooldown, 2)
        # 2 rect
        self.rect(self.x_pos + 335, self.y_pos - 50, 50, 25, self.current_profile.ship_cooldown, 3)
        # 3 rect
        self.rect(self.x_pos + 390, self.y_pos - 50, 50, 25, self.current_profile.ship_cooldown, 4)
        # 4 rect
        self.rect(self.x_pos + 445, self.y_pos - 50, 50, 25, self.current_profile.ship_cooldown, 5)

    def qtd_bullet_rect(self):
        # 1 rect
        self.rect(self.x_pos - 82, self.y_pos + 100, 50, 25, self.current_profile.ship_qtd_bullet, 2)
        # 2 rect
        self.rect(self.x_pos - 27, self.y_pos + 100, 50, 25, self.current_profile.ship_qtd_bullet, 3)
        # 3 rect
        self.rect(self.x_pos + 27, self.y_pos + 100, 50, 25, self.current_profile.ship_qtd_bullet, 4)
        # 4 rect
        self.rect(self.x_pos + 82, self.y_pos + 100, 50, 25, self.current_profile.ship_qtd_bullet, 5)



    def back(self):
        self.save_profile(self.current_profile)
        self.get_owner().change_state("ProfileMenu")

    def screen_content(self) -> None:

        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())
        self.update_rects()

        x_pos = self.display_width//2
        y_pos = self.display_height//2

        self.text("-=-=STORE=-=-", x_pos-250, 20, 50, "white")

        self.text("Credit:", self.display_width-315, 20, 30, "white")
        self.text("%.1f"%self.current_profile.credit, self.display_width-135, 20, 30, "yellow")

        #velmax
        self.text("Vel. Max:", self.x_pos - 420, self.y_pos - 270, 28, "white")
        self.text("+%d"%self.vel_max_price, self.x_pos - 505, self.y_pos - 250, 25, "green")
        self.text("-%d"%self.vel_max_price, self.x_pos - 200, self.y_pos - 250, 25, "red")

        #damage
        self.text("Damage:", self.x_pos + 300, self.y_pos - 270, 28, "white")
        self.text("+%d"%self.damage_price, self.x_pos + 195, self.y_pos - 250, 25, "green")
        self.text("-%d"%self.damage_price, self.x_pos + 505, self.y_pos - 250, 25, "red")

        #life
        self.text("Life:", self.x_pos - 380, self.y_pos - 120, 28, "white")
        self.text("+%d" % self.life_price, self.x_pos - 505, self.y_pos - 100, 25, "green")
        self.text("-%d" % self.life_price, self.x_pos - 200, self.y_pos - 100, 25, "red")

        # cooldown
        self.text("Cooldown:", self.x_pos + 290, self.y_pos - 120, 28, "white")
        self.text("+%d" % self.cooldown_price, self.x_pos + 195, self.y_pos - 100, 25, "green")
        self.text("-%d" % self.cooldown_price, self.x_pos + 505, self.y_pos - 100, 25, "red")

        #qtd bullet
        self.text("Qtd Bullet:", self.x_pos - 95, self.y_pos+30, 28, "white")
        self.text("+%d" % self.qtd_bullet_price, self.x_pos - 167, self.y_pos + 50, 25, "green")
        self.text("-%d" % self.qtd_bullet_price, self.x_pos + 143, self.y_pos + 50, 25, "red")

    def rect(self, x: int, y: int, width: int, heigth: int, profile_value: int, green_value: int):
        color = "gray" if (profile_value < green_value) else "green"
        pygame.draw.rect(self.get_display(), color, (x, y, width, heigth))


    def handle_update(self) -> None:
        pygame.display.update()
        self.background()
        self.screen_content()
        pygame.display.update()

    @property
    def current_profile(self) -> Profile:
        return self.__current_profile

    @property
    def vel_max_price(self):
        return self.__vel_max_price

    @property
    def damage_price(self):
        return self.__damage_price

    @property
    def life_price(self):
        return self.__life_price

    @property
    def cooldown_price(self):
        return self.__cooldown_price

    @property
    def qtd_bullet_price(self):
        return self.__qtd_bullet_price

    @property
    def x_pos(self):
        return self.display_width//2

    @property
    def y_pos(self):
        return self.display_height//2



