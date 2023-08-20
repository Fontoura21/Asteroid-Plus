import pygame
from Utility.Utils.utils import *
from Entities.MovingEntities.MovingEntity import MovingEntity
from Entities.MovingEntities.Bullet.Bullet import Bullet
from math import cos, sin, radians
from os import path
from time import time

pasta = get_folder_versao_top(__file__, 3)

class Ship(MovingEntity):
    def __init__(self, game,
                 speed: float,
                 vel_max: float,
                 cooldown: float,
                 life: int,
                 damage: int,
                 qtd_bullet: int) -> None:
        

        #tempo do ultimo tiro
        self.__last_shoot = 0

        #posição inicial
        x = pygame.display.Info().current_w // 2
        y = pygame.display.Info().current_h // 2

        #direção, impulso e rotação inicial
        self.__damage = damage
        self.__qtd_bullet = qtd_bullet
        self.__cooldown = cooldown
        self.__life = life
        self.__vel_max = vel_max
        self.__speed = speed
        self.__dx = 0
        self.__dy = 0

        #indica se esta acelerando
        self.__boost = False
        self.__smoke_time = 0

        #indica se está invulneravel
        self.__invunerable = False
        self.__invunerable_time = time()
        self.__change_color_time = time()
        self.__blue = False #indica se está cinza

        #carrega imagem 
        self.__bullet_image = pygame.image.load(pasta+"//Images//ship_images//ship_bullet.png")
        image = pygame.image.load(pasta+"//Images//ship_images//boost_blue_ship.png")
        self.__blue_boost_ship_img = pygame.transform.rotate(image, -90)
        image = pygame.image.load(pasta+"//Images//ship_images//blue_ship.png")
        self.__blue_ship_img = pygame.transform.rotate(image, -90)
        image = pygame.image.load(pasta+"//Images//ship_images//boost_ship.png")
        self.__boost_ship_img = pygame.transform.rotate(image, -90)
        image = pygame.image.load(pasta+"//Images//ship_images//ship.png")
        self.__ship_img = pygame.transform.rotate(image, -90)
        image = pygame.image.load(pasta+"//Images//ship_images//ship.png")
        o_image = pygame.transform.rotate(image, -90)
        super().__init__(game, self.speed, 90, o_image, (x, y))


    def user_input(self) -> None:
        keys = pygame.key.get_pressed()

        #tecla W -> acelera
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.accelerate()
            if (not self.boost):
                self.game.get_sound_mixer().play_boost_sfx()
            self.__boost = True
            self.add_smoke_effect()
        else:
            self.game.get_sound_mixer().boost_sfx.stop()
            self.__boost = False
            self.__smoke_time = time()

        #tecla a -> rotaciona no sentido antihorario
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            d = self.direction + 3.75
            self.set_direction(d)

        #tecla d -> rotaciona no sentido horario
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            d = self.direction - 3.75
            self.set_direction(d)

        if (keys[pygame.K_SPACE]):

            self.shoot()

    def add_smoke_effect(self):
        if ((time() - self.__smoke_time) > 0.05):
            x = self.x - cos(radians(self.direction))*13
            y = self.y + sin(radians(self.direction))*13
            self.game.get_animation_effects_manager().add_smoke_effect(game=self.game,
                                                                        position=(x,y),
                                                                        scale=(18,18),
                                                                        looping=False)
            self.__smoke_time = time()


    #metodo que chama bulet, com o tempo minimo entre eles de self.cooldown sec
    def shoot(self) -> None:
        strait_front_bullet = Bullet(game = self,
                                    position = (self.x, self.y),
                                    direction = self.direction,
                                    speed = 10,
                                    damage = self.damage,
                                    color = "yellow",
                                    lifetime = 2,
                                    img=self.__bullet_image)
        
        strait_back_bullet = Bullet(game = self,
                                    position = (self.x, self.y),
                                    direction = self.direction+180,
                                    speed = 10,
                                    damage = self.damage,
                                    color = "yellow",
                                    lifetime = 2,
                                    img=self.__bullet_image)

        top_left_bullet = Bullet(game = self,
                                position = (self.x, self.y),
                                direction = self.direction+30,
                                speed = 10,
                                damage = self.damage,
                                color = "yellow",
                                lifetime = 2,
                                img=self.__bullet_image)

        top_rigth_bullet =  Bullet(game = self,
                                position = (self.x, self.y),
                                direction = self.direction-30,
                                speed = 10,
                                damage = self.damage,
                                color = "yellow",
                                lifetime = 2,
                                img=self.__bullet_image)

        botton_left_bullet = Bullet(game = self,
                                position = (self.x, self.y),
                                direction = self.direction+135,
                                speed = 10,
                                damage = self.damage,
                                color = "yellow",
                                lifetime = 2,
                                img=self.__bullet_image)

        botton_rigth_bullet = Bullet(game = self,
                                position = (self.x, self.y),
                                direction = self.direction-135,
                                speed = 10,
                                damage = self.damage,
                                color = "yellow",
                                lifetime = 2,
                                img=self.__bullet_image)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if ((time() - self.last_shoot) > self.cooldown):
                self.game.get_sound_mixer().play_bullet_sfx()
                
                if (self.qtd_bullet == 1):
                    self.game.all_sprites.add(strait_front_bullet)
                    self.game.ship_bullet_group.add(strait_front_bullet)

                elif (self.qtd_bullet == 2):
                    self.game.all_sprites.add(strait_front_bullet)
                    self.game.all_sprites.add(strait_back_bullet)
                    self.game.ship_bullet_group.add(strait_front_bullet)
                    self.game.ship_bullet_group.add(strait_back_bullet)

                elif (self.qtd_bullet == 3):
                    self.game.all_sprites.add(strait_front_bullet)
                    self.game.all_sprites.add(top_left_bullet)
                    self.game.all_sprites.add(top_rigth_bullet)

                    self.game.ship_bullet_group.add(strait_front_bullet)
                    self.game.ship_bullet_group.add(top_left_bullet)
                    self.game.ship_bullet_group.add(top_rigth_bullet)

                elif (self.qtd_bullet == 4):
                    self.game.all_sprites.add(strait_front_bullet)
                    self.game.all_sprites.add(top_left_bullet)
                    self.game.all_sprites.add(top_rigth_bullet)
                    self.game.all_sprites.add(strait_back_bullet)

                    self.game.ship_bullet_group.add(strait_front_bullet)
                    self.game.ship_bullet_group.add(top_left_bullet)
                    self.game.ship_bullet_group.add(top_rigth_bullet)
                    self.game.ship_bullet_group.add(strait_back_bullet)

                elif (self.qtd_bullet == 5):
                    self.game.all_sprites.add(strait_front_bullet)
                    self.game.all_sprites.add(top_left_bullet)
                    self.game.all_sprites.add(top_rigth_bullet)
                    self.game.all_sprites.add(botton_left_bullet)
                    self.game.all_sprites.add(botton_rigth_bullet)

                    self.game.ship_bullet_group.add(strait_front_bullet)
                    self.game.ship_bullet_group.add(top_left_bullet)
                    self.game.ship_bullet_group.add(top_rigth_bullet)
                    self.game.ship_bullet_group.add(botton_left_bullet)
                    self.game.ship_bullet_group.add(botton_rigth_bullet)


                self.__last_shoot = time()

    #acelera
    def accelerate(self) -> None:
        self.__dx += cos(radians(self.direction)) * self.speed/8
        self.__dy += sin(radians(-self.direction)) * self.speed/8

        if (abs(self.dx) > self.vel_max):
            self.__dx = -self.vel_max if (self.dx < 0) else self.vel_max
        if (abs(self.dy) >= self.vel_max):
            self.__dy = -self.vel_max if (self.dy < 0) else self.vel_max

    #atualiza o impulso e a rotação
    def update_position(self) -> None:
        #diminui a rotação e o impulso, confor o metodo update é chamado
        self.__dx /= 1.01
        self.__dy /= 1.01

        #altera x e y da nave, conforme a inpulso e a diração
        x = self.x + self.dx
        y = self.y + self.dy
        self.set_pos(x, y)

    def hit(self) -> None:
        if (not self.invunerable):
            self.game.get_sound_mixer().play_explosion_sfx()
            self.game.get_animation_effects_manager().add_explosion_effect(game=self.game,
                                                                           position=(self.x,self.y),
                                                                           scale=(50, 50),
                                                                           looping=False,
                                                                           speed=8)
            self.__life -= 1
            self.game.get_game_data().set_ship_life(self.life)

            x = self.display_width//2
            y = self.display_height//2
            self.set_pos(x, y)
            self.set_direction(90)
            self.reset_speed()

            self.__invunerable = True
            self.__invunerable_time = time()
    
    def blink(self) -> None:
        if ((time() - self.change_color_time) >= 0.4):
            self.__blue = True if (self.blue == False) else False
            self.__change_color_time = time()

    def check_invunerable(self) -> None:
        if (self.invunerable):

            self.blink()

            if ((time() - self.invunerable_time) >= 2):
                self.__invunerable = False
                self.__blue = False

    def change_color(self):
        if (self.blue):
            if (self.boost):
                image = self.__blue_boost_ship_img
            else:
                image = self.__blue_ship_img
        else:
            if (self.boost):
                image = self.__boost_ship_img
            else:
                image = self.__ship_img

        self.set_original_image(image)

    #metodo UPDATE, todo sprite deve ter
    # é chamado com o o self.all_sprites é atualizado(esta no asteroid game)
    def update(self) -> None:
        self.check_invunerable()
        self.change_color()
        self.user_input()
        super().update()

    def reset_speed(self):
        self.__dx = 0
        self.__dy = 0

    @property
    def boost(self):
        return self.__boost

    @property
    def qtd_bullet(self):
        return self.__qtd_bullet

    @property
    def damage(self):
        return self.__damage

    @property
    def change_color_time(self):
        return self.__change_color_time

    @property
    def blue(self):
        return self.__blue

    @property
    def invunerable(self):
        return self.__invunerable

    @property
    def invunerable_time(self):
        return self.__invunerable_time

    @property
    def life(self):
        return self.__life

    @property
    def cooldown(self):
        return self.__cooldown

    @property
    def speed(self):
        return self.__speed

    @property
    def vel_max(self):
        return self.__vel_max

    @property
    def dx(self):
        return self.__dx

    @property
    def dy(self):
        return self.__dy

    @property
    def last_shoot(self):
        return self.__last_shoot


