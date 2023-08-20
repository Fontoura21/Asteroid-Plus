import pygame
from os import path
from States.State import State
from Profiles.Profile import Profile
from Entities.MovingEntities.Ship.Ship import Ship
from CollisionManager.CollisionManager import CollisionManager
from Entities.MovingEntities.Asteroid.Asteroid import Asteroid
from Entities.MovingEntities.BasicEnemy.BasicEnemy import BasicEnemy
from Entities.Button.Button import Button
from time import time

pasta = path.dirname(path.dirname(__file__))


class NormalLevel(State):
    def __init__(self, owner) -> None:
        super().__init__(owner)

        self.__colision_manager = CollisionManager(self)

        self.__profile: Profile = self.get_game_data().profile

        #pause data
        self.__pause = False
        self.__pause_time = time()
        self.__click_buton_time = time()
        self.__pause_button_group = pygame.sprite.Group()
        self.__fade = pygame.Surface((self.display_width, self.display_height), pygame.SRCALPHA)
        self.__fade.set_alpha(50)
        pygame.draw.rect(self.__fade, "gray", (0, 0, self.display_width, self.display_height))
        self.create_button()

        self.__ship_group = pygame.sprite.Group()
        self.__ship_bullet_group = pygame.sprite.Group()
        self.__asteroid_group = pygame.sprite.Group()
        self.__basic_enemy_group = pygame.sprite.Group()
        self.__basic_enemy_bullet_group = pygame.sprite.Group()

        self.__add_asteroid_time = time()
        self.__add_basic_enemy_time = time()

        life = (3+self.profile.ship_life-1) if (self.get_game_data().ship_life == None) else self.get_game_data().ship_life
        self.get_game_data().set_ship_life(life)

        level = 1 if (self.level == None) else self.level
        self.get_game_data().set_level(level)

        enemies_destroyed = 0 if (self.enemies_destroyed == None) else self.enemies_destroyed
        self.set_enemies_destroyed(enemies_destroyed)

        self.__next_level_time = time()+30

        self.__basic_enemy_img = pygame.image.load(pasta+"//Images//BasicEnemy.png")
        self.__list_asteroid_img = self.load_asteroids_images()

        self.add_ship()

        asteroid = Asteroid(game = self, lst_imgs = self.__list_asteroid_img, size = 2)
        self.all_sprites.add(asteroid)
        self.asteroid_group.add(asteroid)

        self.__clock = pygame.time.Clock()

    def load_asteroids_images(self) -> list:
        asteroid_imgs_list = list()
        for n in range(1, 8):
            image = pygame.image.load(pasta+f"//Images//asteroid_images//asteroid_{n}.png")
            asteroid_imgs_list.append(image)

        return asteroid_imgs_list


    def add_ship(self) -> None:
        vel_max = 10*(1.2)**(self.profile.ship_vel_max-1)
        cooldown = 0.8 - (0.15 * (self.profile.ship_cooldown-1))
        damage = self.profile.ship_damage
        qtd_bullet = self.profile.ship_qtd_bullet

        life = self.get_game_data().ship_life

        self.__ship = Ship(game = self,
                           speed = vel_max*0.3,
                           vel_max = vel_max,
                           cooldown = cooldown,
                           life = life,
                           damage = damage,
                           qtd_bullet = qtd_bullet)

        self.all_sprites.add(self.ship)
        self.ship_group.add(self.ship)
    
    def add_asteroid(self):
        addtime = 10*(0.9**(self.level - 1))
        if (time() - self.add_asteroid_time) >= addtime:
            asteroid = Asteroid(game = self,
                                lst_imgs=self.__list_asteroid_img,
                                size = 2)
            
            self.all_sprites.add(asteroid)
            self.asteroid_group.add(asteroid)
            self.__add_asteroid_time = time()


    def add_basic_enemy(self):
        basic_enemy_time = 15*(0.9**(self.level - 1))
        if (time() - self.add_basic_enemy_time) >= basic_enemy_time:
            basic_enemy = BasicEnemy(game = self,
                                    img = self.__basic_enemy_img,
                                    life = 1)
            self.all_sprites.add(basic_enemy)
            self.basic_enemy_group.add(basic_enemy)
            self.__add_basic_enemy_time = time()

    def create_button(self):
        x_pos = self.display_width//2
        y_pos = self.display_height//2

        resume = Button(self, x_pos-310, y_pos+10, 300, 100, "Resume", True, self.unpause)
        self.__pause_button_group.add(resume)

        quit = Button(self, x_pos+10, y_pos+10, 300, 100, "Quit", True, self.quit)
        self.__pause_button_group.add(quit)

    def quit(self):
        self.reset_data()
        self.get_owner().sound_mixer.play_theme_music()
        self.get_owner().change_state("ProfileMenu")

    def reset_data(self):
        life = 3 + self.get_game_data().profile.ship_life-1
        self.get_game_data().set_ship_life(life)
        self.get_game_data().set_enemies_destroyed(0)
        self.get_game_data().set_level(1)

    def screen_content(self):

        x_pos = self.display_width//2
        y_pos = self.display_width//2

        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())

        self.text("Level:", x_pos-85, 15, 25, "white")
        self.text(str(self.level), x_pos+45, 15, 25, "yellow")
        self.text("Next Level in %d sec"%int(self.next_level_time-time()), 10, self.display_height-35, 25, "white")

        self.text("Enemies Destroyed:", 10, 10, 25, "white")
        self.text(str(self.enemies_destroyed), 390, 10, 25, "yellow")

        self.text("Score:", 10, 35, 25, "white")
        self.text(str(self.score), 140, 35, 25, "yellow")

        self.text("Life:", self.display_width-150, 10, 25, "white")
        self.text(str(self.ship.life),self.display_width-40, 10, 25, "yellow")

        self.text("Press P to pause", self.display_width-350, self.display_height-35, 25, "yellow")

    def detect_pause(self):
        keys = pygame.key.get_pressed()
        if ((time() - self.__click_buton_time) > 0.5):
            if (keys[pygame.K_p]):
                    if (self.__pause):
                        self.unpause()
                    else:
                        self.pause()

                    self.__click_buton_time = time()

    def unpause(self):
        self.__pause = False
        pygame.mixer.unpause()
        time_dif = (time() - self.__pause_time)
        self.__next_level_time = self.next_level_time+(time_dif)

    def pause(self):
        pygame.mixer.pause()
        self.get_owner().sound_mixer.play_pause_sfx()
        self.get_display().blit(self.__fade, (0, 0))
        self.__pause_time = time()
        self.__pause = True

    def pause_content(self):
        self.text("-=-=PAUSE=-=-", (self.display_width//2)-220, (self.display_height//2)-200, 40, "yellow")
        self.text("Data isnt't saved if quit", (self.display_width//2)-260, (self.display_height//2)-30, 25, "red")
        self.__pause_button_group.update()
        self.__pause_button_group.draw(self.get_display())

    def level_transition(self):
        if (self.next_level_time-time() <= 0):
            self.__next_level_time = time() + 30
            self.get_game_data().set_level(self.level+1)
            if ((self.level % 5) != 0):
                self.get_sound_mixer().play_lvl_up_sfx()

            if ((self.level % 5) == 0):
                self.update_score()
                self.get_owner().change_state("BossTransition")

    def set_enemies_destroyed(self, num: int) -> None:
        self.get_game_data().set_enemies_destroyed(num)

    def update_score(self) -> None:
        self.get_game_data().set_score(self.enemies_destroyed*self.level)

    def handle_update(self):
        self.clock.tick(60)
        self.detect_pause()

        pygame.display.update()
        if (not self.__pause):
            self.background(0.2*8)
            self.screen_content()
            self.add_asteroid()
            self.add_basic_enemy()
            self.collision_manager.collisions_normal_level()
            self.update_score()
            self.level_transition()
        else:
            self.pause_content()
        pygame.display.update()
        

    @property
    def collision_manager(self):
        return self.__colision_manager

    @property
    def level(self):
        return self.get_game_data().level

    @property
    def score(self):
        return self.get_game_data().score

    @property
    def enemies_destroyed(self):
        return self.get_game_data().enemies_destroyed

    @property
    def clock(self):
        return self.__clock

    @property
    def ship(self):
        return self.__ship

    @property
    def profile(self):
        return self.__profile

    @property
    def ship_group(self):
        return self.__ship_group

    @property
    def ship_bullet_group(self):
        return self.__ship_bullet_group

    @property
    def asteroid_group(self):
        return self.__asteroid_group

    @property
    def basic_enemy_group(self):
        return self.__basic_enemy_group

    @property
    def basic_enemy_bullet_group(self):
        return self.__basic_enemy_bullet_group

    @property
    def next_level_time(self):
        return self.__next_level_time
    
    @property
    def add_asteroid_time(self):
        return self.__add_asteroid_time
    
    @property
    def add_basic_enemy_time(self):
        return self.__add_basic_enemy_time
