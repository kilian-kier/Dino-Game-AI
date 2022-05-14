import pygame
import sprite
import config


ground_image = pygame.transform.scale2x(sprite.load_image("ground.png"))


class Ground:
    IMAGE = ground_image
    VEL = config.SPEED
    WIDTH = IMAGE.get_width()

    def __init__(self):
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        elif self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        config.WIN.blit(self.IMAGE, (self.x1, config.GROUND))
        config.WIN.blit(self.IMAGE, (self.x2, config.GROUND))
