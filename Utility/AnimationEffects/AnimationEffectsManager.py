import pygame
import fnmatch
import os
from Utility.AnimationEffects.AnimationEffect import AnimationEffect

pasta = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
explosion_assets_dir = pasta+"//Images//Frames//ExplosionFrames"
boss_explosion_assets_dir = pasta+"//Images//Frames//BossExplosionFrames"
smoke_assets_dir = pasta+"//Images//Frames//SmokeFrames"
laser_assets_dir = pasta+"//Images//Frames//LaserFrames"

class AnimationEffectsManager:
    def __init__(self):
        self.__explosion_imgs_list =      self.load_list_imgs(explosion_assets_dir)
        self.__boss_explosion_imgs_list = self.load_list_imgs(boss_explosion_assets_dir)
        self.__smoke_imgs_list =          self.load_list_imgs(smoke_assets_dir)
        self.__laser_imgs_list =          self.load_list_imgs(laser_assets_dir)

    def add_explosion_effect(self, game, position: tuple, scale: tuple, looping: bool, speed: int) -> AnimationEffect:
        return AnimationEffect(game, position, scale, speed, looping, self.__explosion_imgs_list)

    def add_boss_explosion_effect(self, game, position: tuple, scale: tuple, looping: bool) -> AnimationEffect:
        return AnimationEffect(game, position, scale, 10, looping, self.__boss_explosion_imgs_list)

    def add_smoke_effect(self, game, position: tuple, scale: tuple, looping: bool) -> AnimationEffect:
        return AnimationEffect(game, position, scale, 5, looping, self.__smoke_imgs_list)

    def add_laser_effect(self, game, position: tuple, scale: tuple, direction: int, looping: bool) -> AnimationEffect:
        return AnimationEffect(game, position, scale, 8, looping, self.__laser_imgs_list, direction)

    def load_list_imgs(self, frames_dir: str) -> list:
        imgs_list = list()
        n_images = len(fnmatch.filter(os.listdir(frames_dir), "*.png"))+1

        for n in range(1, n_images):
            img = pygame.image.load(frames_dir+f"//{n}.png")
            imgs_list.append(img)

        return imgs_list
