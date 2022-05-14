import config
import pygame
import sprite
import random


cactus_images = sprite.load_sprite_sheet('cacti.png', 4, 1)


class Cactus:
    IMAGES = cactus_images
    VEL = config.SPEED

    def __init__(self, x):
        self.x = x
        self.y = config.GROUND - self.IMAGES[0].get_height() + 25
        self.img = self.IMAGES[random.randint(0, 3)]
        self.passed = False

    def move(self):
        self.x -= self.VEL

    def draw(self):
        config.WIN.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        """ dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.img)
        offset_x = self.x - dino.x
        offset_y = self.y - int(dino.y)

        point = cactus_mask.overlap(dino_mask, (offset_x, offset_y))
        print((dino.x + dino.img.get_width(), dino.y), (self.x, self.y), point)
        return point """
        dino_rect = pygame.rect.Rect(
            (dino.x, dino.y, dino.img.get_width(), dino.img.get_height()))
        cactus_rect = pygame.rect.Rect(
            (self.x, self.y, self.img.get_width(), self.img.get_height()))
        if cactus_rect.colliderect(dino_rect):
            return True
        else:
            return False
