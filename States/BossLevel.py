import pygame
from States.State import State
from Profiles.Profile import Profile
from Entities.MovingEntities.Ship.Ship import Ship
from Entities.MovingEntities.TankBoss.TankBoss import TankBoss
from Entities.MovingEntities.CannonBoss.CannonBoss import CannonBoss 
from Entities.MovingEntities.FollowBoss.FollowBoss import FollowBoss 
from Entities.Button.Button import Button
from CollisionManager.CollisionManager import CollisionManager
from random import randint
from time import time

class BossLevel(State):
    def __init__(self, owner) -> None:
        super().__init__(owner)

        self.__collision_manager = CollisionManager(self)

        self.__profile: Profile = self.get_game_data().profile

        #pause data
        self.__pause = False
        self.__click_button_time = time()
        self.__pause_button_group = pygame.sprite.Group()
        self.__fade = pygame.Surface((self.display_width, self.display_height), pygame.SRCALPHA)
        self.__fade.set_alpha(50)
        pygame.draw.rect(self.__fade, "gray", (0, 0, self.display_width, self.display_height))
        self.create_button()

        initial_pos = (self.display_width//2, 30)
        tankboss = TankBoss(game=self, life=20, position=initial_pos)
        cannonboss = CannonBoss(game=self, life=15, position=initial_pos)
        followboss = FollowBoss(game=self, life=10, position=initial_pos)
        self.__boss_list = [tankboss, cannonboss, followboss]

        self.__ship_group = pygame.sprite.Group()
        self.__ship_bullet_group = pygame.sprite.Group()
        self.__boss_group = pygame.sprite.Group()
        self.__boss_bullet_group = pygame.sprite.Group()

        life = (3+self.profile.ship_life-1) if (self.get_game_data().ship_life == None) else self.get_game_data().ship_life
        self.get_game_data().set_ship_life(life)

        level = 1 if (self.level == None) else self.level
        self.get_game_data().set_level(level)

        enemies_destroyed = 0 if (self.enemies_destroyed == None) else self.enemies_destroyed
        self.set_enemies_destroyed(enemies_destroyed)

        level = 1 if (self.level == None) else self.level
        self.get_game_data().set_level(level)

        self.add_ship()
        self.sort_boss()

        self.__clock = pygame.time.Clock()

    def update_score(self):
        self.get_game_data().set_score(self.enemies_destroyed*self.level)

    def sort_boss(self) -> None:
        self.__boss = self.boss_list[randint(0, len(self.boss_list)-1)]
        self.__original_boss_life = self.boss.life
        self.all_sprites.add(self.boss)
        self.boss_group.add(self.boss)

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

    def render_boss_life(self):
        x_poss = self.display_width//2
        y_poss = self.display_height//2

        width = 360

        pygame.draw.rect(self.get_display(), "gray", (x_poss-width//2, self.display_height-40, width, 15))
        pygame.draw.rect(self.get_display(), "red", (x_poss-width//2, self.display_height-40, (width//self.original_boss_life)*self.boss.life, 15))

    def screen_content(self):

        self.render_boss_life()

        x_pos = self.display_width//2
        y_pos = self.display_width//2

        self.all_sprites.update()
        self.all_sprites.draw(self.get_display())

        self.text("Level:", x_pos-85, 15, 25, "white")
        self.text(str(self.level), x_pos+45, 15, 25, "yellow")

        self.text("Enemies Destroyed:", 10, 10, 25, "white")
        self.text(str(self.enemies_destroyed), 390, 10, 25, "yellow")

        self.text("Score:", 10, 35, 25, "white")
        self.text(str(self.score), 140, 35, 25, "yellow")

        self.text("Life:", self.display_width-150, 10, 25, "white")
        self.text(str(self.ship.life),self.display_width-40, 10, 25, "yellow")

        self.text("BOSS LIFE", x_pos-120, self.display_height-90, 30, "red")

        self.text("Press P to pause", self.display_width-350, self.display_height-35, 25, "yellow")

    def detect_pause(self):
        keys = pygame.key.get_pressed()
        if ((time() - self.__click_button_time) > 0.5):
            if (keys[pygame.K_p]):
                    if (self.__pause):
                        self.unpause()
                    else:
                        self.pause()

                    self.__click_button_time = time()

    def unpause(self):
        self.__pause = False
        pygame.mixer.unpause()

    def pause(self):
        pygame.mixer.pause()
        self.get_owner().sound_mixer.play_pause_sfx()
        self.get_display().blit(self.__fade, (0, 0))
        self.__pause = True

    def pause_content(self):
        self.text("-=-=PAUSE=-=-", (self.display_width//2)-220, (self.display_height//2)-200, 40, "yellow")
        self.text("Data isnt't saved if quit", (self.display_width//2)-260, (self.display_height//2)-30, 25, "red")
        self.__pause_button_group.update()
        self.__pause_button_group.draw(self.get_display())

    def handle_update(self):
        self.clock.tick(60)
        self.detect_pause()
        pygame.display.update()
        if (not self.__pause):
            self.background(speed=0.2*8)
            self.screen_content()
            self.update_score()
            self.collision_manager.collisions_boss_level()
        else:
            self.pause_content()
        pygame.display.update()

    def set_enemies_destroyed(self, num: int) -> None:
        self.get_game_data().set_enemies_destroyed(num)

    @property
    def original_boss_life(self):
        return self.__original_boss_life

    @property
    def collision_manager(self):
        return self.__collision_manager

    @property
    def enemies_destroyed(self):
        return self.get_game_data().enemies_destroyed

    @property
    def score(self):
        return self.get_game_data().score

    @property
    def level(self):
        return self.get_game_data().level

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
    def boss_list(self):
        return self.__boss_list

    @property
    def boss_group(self):
        return self.__boss_group

    @property
    def boss(self):
        return self.__boss

    @property
    def boss_bullet_group(self):
        return self.__boss_bullet_group
