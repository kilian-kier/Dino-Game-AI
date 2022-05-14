import pygame
import sprite
import config


class Dino:
    IMAGES = sprite.load_sprite_sheet('dino.png', 4, 0.6)
    ANIMATION_TIME = 5
    JUMP_N = 10.5

    def __init__(self):
        self.x = 40
        self.y = config.GROUND - self.IMAGES[0].get_height() + 25
        self.vel = 0
        self.mass = 1
        self.is_jumping = False
        self.img_count = 0
        self.img = self.IMAGES[0]

    def jump(self):
        if not self.is_jumping:
            self.vel = self.JUMP_N
            self.is_jumping = True

    def move(self):
        if self.is_jumping:
            if self.vel >= -self.JUMP_N:
                self.y -= (self.vel * abs(self.vel)) * 0.5
                self.vel -= 1.5
            else:
                self.vel = 0
                self.is_jumping = False

    def draw(self):
        if self.is_jumping:
            self.img = self.IMAGES[0]
            self.img_count = 0
        else:
            self.img_count += 1
            if self.img_count <= self.ANIMATION_TIME:
                self.img = self.IMAGES[1]
            elif self.img_count <= self.ANIMATION_TIME * 2:
                self.img = self.IMAGES[2]
            elif self.img_count <= self.ANIMATION_TIME * 3:
                self.img = self.IMAGES[1]
                self.img_count = 0
        config.WIN.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
