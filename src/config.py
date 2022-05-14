import pygame
from ground import ground_image

pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 500
STAT_FONT = pygame.font.SysFont("comicsans", 32)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Dino Game AI")
SPEED = 12
GEN = 0
HIGH_SCORE = 0
GROUND = WIN_HEIGHT - ground_image.get_height()
